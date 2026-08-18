#!/usr/bin/env python3
"""AI Flaky Test Detector — feed JUnit XML reports from multiple runs and let
Claude identify flaky tests, classify root causes, and suggest fixes.

Flaky tests are one of the biggest time-sinks in QA. They erode trust in the
test suite and slow down CI pipelines. This tool parses JUnit XML results from
several runs, spots tests that flip between pass and fail, and uses Claude to
analyze *why* they're flaky and *how* to fix them.

Usage:
    # Point at a directory of JUnit XML files from multiple CI runs
    python detect_flaky_tests.py --reports-dir ./junit-reports

    # Or pass individual XML files
    python detect_flaky_tests.py --files run1.xml run2.xml run3.xml

    # Generate sample data to try it out
    python detect_flaky_tests.py --demo
"""

import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

import anthropic

SYSTEM_PROMPT = """\
You are a senior QA engineer specializing in test reliability and CI/CD
stability. You are given a summary of test results across multiple test runs.

Your job:
1. Identify flaky tests (tests that pass in some runs and fail in others).
2. For each flaky test, classify the likely root cause into one of:
   - TIMING: race conditions, sleeps, timeouts, async waits
   - ORDER_DEPENDENT: test relies on state from another test
   - ENVIRONMENT: external service, network, port conflicts, file system
   - RESOURCE_LEAK: unclosed connections, memory, file handles
   - DATA_DEPENDENT: shared mutable test data, random values, timestamps
   - CONCURRENCY: thread safety, shared state in parallel runs
3. Provide a concrete fix suggestion for each flaky test.
4. Give an overall health score (0-100) for the test suite.
5. If failure messages are provided, use them to refine your analysis.

Respond in this JSON structure (no markdown fences):
{
  "health_score": <int 0-100>,
  "total_tests": <int>,
  "total_runs": <int>,
  "flaky_tests": [
    {
      "test_name": "<fully qualified test name>",
      "pass_count": <int>,
      "fail_count": <int>,
      "flakiness_rate": "<percentage>",
      "likely_cause": "<one of the categories above>",
      "evidence": "<what in the data points to this cause>",
      "fix_suggestion": "<actionable fix>"
    }
  ],
  "summary": "<2-3 sentence overall assessment>"
}
"""


def parse_junit_xml(filepath):
    """Parse a JUnit XML file and return a list of test results.

    Each result is a dict with keys: name, classname, status, message.
    """
    results = []
    try:
        tree = ET.parse(filepath)
    except ET.ParseError as e:
        print(f"Warning: could not parse {filepath}: {e}", file=sys.stderr)
        return results

    root = tree.getroot()
    # Handle both <testsuites><testsuite>... and bare <testsuite>...
    testcases = root.iter("testcase")

    for tc in testcases:
        name = tc.get("name", "unknown")
        classname = tc.get("classname", "")
        full_name = f"{classname}::{name}" if classname else name
        time_taken = tc.get("time", "0")

        failure = tc.find("failure")
        error = tc.find("error")
        skipped = tc.find("skipped")

        if skipped is not None:
            status = "skipped"
            message = skipped.get("message", "")
        elif failure is not None:
            status = "failed"
            message = failure.get("message", "")
            # Include first few lines of the failure body for context
            body = (failure.text or "").strip()
            if body:
                lines = body.split("\n")[:5]
                message = f"{message}\n{''.join(lines)}" if message else "\n".join(lines)
        elif error is not None:
            status = "error"
            message = error.get("message", "")
        else:
            status = "passed"
            message = ""

        results.append({
            "name": full_name,
            "status": status,
            "time": time_taken,
            "message": message[:300],  # truncate long messages
        })

    return results


def collect_results(reports_dir=None, files=None):
    """Collect test results from JUnit XML files.

    Returns a dict mapping run_label -> list of test result dicts.
    """
    runs = {}
    xml_files = []

    if reports_dir:
        p = Path(reports_dir)
        xml_files = sorted(p.glob("**/*.xml"))
        if not xml_files:
            print(f"No XML files found in {reports_dir}", file=sys.stderr)
            sys.exit(1)
    elif files:
        xml_files = [Path(f) for f in files]

    for i, f in enumerate(xml_files, start=1):
        label = f"run_{i} ({f.name})"
        results = parse_junit_xml(f)
        if results:
            runs[label] = results

    return runs


def build_summary(runs):
    """Build a per-test summary across all runs."""
    test_history = defaultdict(lambda: {"passed": 0, "failed": 0, "error": 0,
                                        "skipped": 0, "messages": []})
    for run_label, results in runs.items():
        for r in results:
            entry = test_history[r["name"]]
            entry[r["status"]] = entry.get(r["status"], 0) + 1
            if r["message"] and r["status"] in ("failed", "error"):
                entry["messages"].append(f"[{run_label}] {r['message']}")

    # Identify flaky = has both passes and failures
    summary = {
        "total_runs": len(runs),
        "total_unique_tests": len(test_history),
        "tests": {},
    }

    for test_name, counts in test_history.items():
        total_exec = counts["passed"] + counts["failed"] + counts["error"]
        if total_exec == 0:
            continue
        fail_total = counts["failed"] + counts["error"]
        is_flaky = counts["passed"] > 0 and fail_total > 0

        summary["tests"][test_name] = {
            "passed": counts["passed"],
            "failed": counts["failed"],
            "error": counts["error"],
            "skipped": counts["skipped"],
            "is_flaky": is_flaky,
            "failure_messages": counts["messages"][:3],  # keep top 3
        }

    return summary


def analyze_with_claude(summary):
    """Send the test summary to Claude for flaky test analysis."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: set ANTHROPIC_API_KEY environment variable.",
              file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic()

    # Build a concise prompt
    flaky_count = sum(1 for t in summary["tests"].values() if t["is_flaky"])
    always_fail = sum(
        1 for t in summary["tests"].values()
        if t["passed"] == 0 and (t["failed"] + t["error"]) > 0
    )

    prompt = f"""Here are test results across {summary['total_runs']} runs \
({summary['total_unique_tests']} unique tests, {flaky_count} flaky, \
{always_fail} always-failing):

{json.dumps(summary['tests'], indent=2)}

Analyze the flaky tests and provide your assessment."""

    print(f"\nAnalyzing {flaky_count} flaky tests across "
          f"{summary['total_runs']} runs...\n")

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
    except anthropic.AuthenticationError:
        print("Error: invalid ANTHROPIC_API_KEY.", file=sys.stderr)
        sys.exit(1)

    return response.content[0].text


def generate_demo_data():
    """Generate sample JUnit XML files to demonstrate the tool."""
    import random
    import tempfile

    demo_dir = Path(tempfile.mkdtemp(prefix="flaky_demo_"))
    print(f"Generating demo JUnit reports in: {demo_dir}\n")

    tests = [
        ("test_login", "TestAuth", "always_pass"),
        ("test_logout", "TestAuth", "always_pass"),
        ("test_checkout_flow", "TestCart", "flaky_timing"),
        ("test_search_results", "TestSearch", "flaky_data"),
        ("test_file_upload", "TestUpload", "flaky_env"),
        ("test_payment", "TestCart", "always_pass"),
        ("test_notification_delivery", "TestNotify", "flaky_timing"),
        ("test_report_export", "TestReports", "always_pass"),
        ("test_concurrent_edits", "TestCollab", "flaky_concurrency"),
        ("test_user_profile", "TestUser", "always_pass"),
    ]

    failure_messages = {
        "flaky_timing": [
            "AssertionError: expected element to be visible within 5s",
            "TimeoutError: server did not respond within 3000ms",
            "AssertionError: status was 'pending', expected 'complete'",
        ],
        "flaky_data": [
            "AssertionError: expected 10 results, got 9",
            "AssertionError: 'Product A' not found in search results",
        ],
        "flaky_env": [
            "ConnectionRefusedError: [Errno 111] Connection refused (port 9222)",
            "OSError: [Errno 28] No space left on device",
        ],
        "flaky_concurrency": [
            "AssertionError: document version mismatch: expected 3, got 2",
            "StaleElementReferenceError: element is no longer attached to DOM",
        ],
    }

    random.seed(42)
    for run_idx in range(1, 6):
        root = ET.Element("testsuite", name="QA Suite",
                          tests=str(len(tests)),
                          timestamp=f"2026-08-{10+run_idx}T10:00:00")

        for test_name, classname, behavior in tests:
            tc = ET.SubElement(root, "testcase", name=test_name,
                               classname=classname,
                               time=f"{random.uniform(0.1, 5.0):.3f}")

            if behavior == "always_pass":
                pass  # no failure element
            elif behavior.startswith("flaky"):
                if random.random() < 0.4:  # 40% chance of failure
                    msg = random.choice(failure_messages[behavior])
                    f = ET.SubElement(tc, "failure", message=msg)
                    f.text = msg

        tree = ET.ElementTree(root)
        filepath = demo_dir / f"junit_run_{run_idx}.xml"
        tree.write(filepath, xml_declaration=True, encoding="unicode")

    return str(demo_dir)


def print_results(raw_response):
    """Pretty-print the analysis results."""
    try:
        data = json.loads(raw_response)
    except json.JSONDecodeError:
        # If Claude didn't return valid JSON, just print the raw text
        print(raw_response)
        return

    score = data.get("health_score", "?")
    print(f"Test Suite Health Score: {score}/100")
    print(f"Runs analyzed: {data.get('total_runs', '?')}")
    print(f"Total tests: {data.get('total_tests', '?')}")
    print()

    flaky = data.get("flaky_tests", [])
    if not flaky:
        print("No flaky tests detected!")
    else:
        print(f"Flaky Tests Found: {len(flaky)}")
        print("=" * 70)
        for t in flaky:
            print(f"\n  {t['test_name']}")
            print(f"    Pass/Fail: {t['pass_count']}/{t['fail_count']}  "
                  f"({t.get('flakiness_rate', 'N/A')})")
            print(f"    Cause:     {t.get('likely_cause', 'unknown')}")
            print(f"    Evidence:  {t.get('evidence', '')}")
            print(f"    Fix:       {t.get('fix_suggestion', '')}")

    print(f"\n{data.get('summary', '')}")


def main():
    parser = argparse.ArgumentParser(
        description="Detect flaky tests from JUnit XML reports using AI"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--reports-dir",
                       help="Directory containing JUnit XML files")
    group.add_argument("--files", nargs="+",
                       help="Individual JUnit XML files")
    group.add_argument("--demo", action="store_true",
                       help="Generate sample data and run analysis")
    args = parser.parse_args()

    if args.demo:
        demo_dir = generate_demo_data()
        args.reports_dir = demo_dir

    runs = collect_results(reports_dir=args.reports_dir, files=args.files)
    if not runs:
        print("No test results found.", file=sys.stderr)
        sys.exit(1)

    print(f"Parsed {len(runs)} test run(s):")
    for label, results in runs.items():
        passed = sum(1 for r in results if r["status"] == "passed")
        failed = sum(1 for r in results if r["status"] in ("failed", "error"))
        print(f"  {label}: {passed} passed, {failed} failed")

    summary = build_summary(runs)
    flaky_count = sum(1 for t in summary["tests"].values() if t["is_flaky"])

    if flaky_count == 0:
        print("\nNo flaky tests detected — all tests are consistently "
              "passing or failing.")
        return

    raw = analyze_with_claude(summary)
    print_results(raw)


if __name__ == "__main__":
    main()
