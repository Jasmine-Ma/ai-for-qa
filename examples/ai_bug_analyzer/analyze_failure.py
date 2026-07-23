"""
AI Bug Analyzer — Feed stack traces and test failure logs to get root cause suggestions.

Usage:
    export ANTHROPIC_API_KEY="your-key-here"

    # Analyze a log file:
    python analyze_failure.py --file test_output.log

    # Pipe output directly:
    pytest --tb=long 2>&1 | python analyze_failure.py

    # Paste a stack trace interactively:
    python analyze_failure.py

Requirements:
    pip install anthropic
"""

import argparse
import sys

import anthropic

SYSTEM_PROMPT = """\
You are a senior QA engineer and debugging expert. Given a test failure log or \
stack trace, provide a concise analysis:

1. **Root Cause** — What most likely caused the failure
2. **Evidence** — The specific lines in the log that support your conclusion
3. **Suggested Fix** — Concrete steps to resolve the issue
4. **Category** — Classify the failure (e.g., assertion error, timeout, \
environment issue, flaky test, missing dependency, data issue)

Be specific and actionable. Reference exact error messages and line numbers \
from the input.
"""

EXAMPLE_FAILURE = """\
============================= FAILURES =============================
_____________ test_create_order_returns_201 _____________

    def test_create_order_returns_201(api_client):
        payload = {"item": "widget", "quantity": 3, "price": 9.99}
>       response = api_client.post("/api/orders", json=payload)

tests/test_orders.py:24:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

    def post(self, url, json=None):
        full_url = self.base_url + url
>       resp = requests.post(full_url, json=json, timeout=5)

src/client.py:18:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

requests.exceptions.ConnectionError: HTTPConnectionPool(host='localhost', port=8080):
Max retries exceeded with url: /api/orders
(Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x...>:
Failed to establish a new connection: [Errno 111] Connection refused'))
"""


def analyze_failure(log_text: str) -> str:
    """Send a failure log to Claude and return the analysis."""
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Analyze this test failure:\n\n{log_text}",
            }
        ],
    )

    return message.content[0].text


def main():
    parser = argparse.ArgumentParser(description="Analyze test failures with AI")
    parser.add_argument("--file", type=str, help="Path to a log file to analyze")
    args = parser.parse_args()

    # Read from file, stdin pipe, or use the built-in example
    if args.file:
        with open(args.file) as f:
            log_text = f.read()
    elif not sys.stdin.isatty():
        log_text = sys.stdin.read()
    else:
        print("No input provided. Using built-in example failure.\n")
        log_text = EXAMPLE_FAILURE

    print("Analyzing failure log...")

    try:
        analysis = analyze_failure(log_text)
    except anthropic.AuthenticationError:
        print("Error: Invalid or missing ANTHROPIC_API_KEY.", file=sys.stderr)
        sys.exit(1)

    print("\n--- Analysis ---\n")
    print(analysis)


if __name__ == "__main__":
    main()
