"""
AI API Tester — Given an OpenAPI spec, auto-generate and run API tests.

Usage:
    export ANTHROPIC_API_KEY="your-key-here"

    # Generate tests from a spec file:
    python smart_api_test.py --spec openapi.json

    # Generate tests from a URL:
    python smart_api_test.py --spec https://petstore3.swagger.io/api/v3/openapi.json

    # Just generate tests without running them:
    python smart_api_test.py --spec openapi.json --generate-only --output test_api.py

Requirements:
    pip install anthropic requests pyyaml
"""

import argparse
import json
import sys
import textwrap

import anthropic
import requests
import yaml

SYSTEM_PROMPT = """\
You are a senior QA engineer specializing in API testing. Given an OpenAPI/Swagger \
specification, generate a complete, runnable pytest test suite.

Follow these rules:
- Use the `requests` library for HTTP calls
- Parameterize the base URL via a pytest fixture
- Test each endpoint's success path and common error paths (400, 401, 404)
- Validate response status codes and JSON schema structure
- Include boundary tests for required fields and parameter constraints
- Add descriptive docstrings for each test
- Group tests by endpoint using test classes
- Output ONLY valid Python code, no markdown fences

Start the file with necessary imports (pytest, requests, json).
"""

EXAMPLE_SPEC = {
    "openapi": "3.0.0",
    "info": {"title": "Todo API", "version": "1.0.0"},
    "paths": {
        "/todos": {
            "get": {
                "summary": "List all todos",
                "responses": {"200": {"description": "A list of todos"}},
            },
            "post": {
                "summary": "Create a todo",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "required": ["title"],
                                "properties": {
                                    "title": {"type": "string", "maxLength": 200},
                                    "completed": {"type": "boolean", "default": False},
                                },
                            }
                        }
                    },
                },
                "responses": {
                    "201": {"description": "Todo created"},
                    "400": {"description": "Invalid input"},
                },
            },
        },
        "/todos/{id}": {
            "get": {
                "summary": "Get a todo by ID",
                "parameters": [
                    {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                ],
                "responses": {
                    "200": {"description": "The todo"},
                    "404": {"description": "Not found"},
                },
            },
            "delete": {
                "summary": "Delete a todo",
                "parameters": [
                    {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                ],
                "responses": {
                    "204": {"description": "Deleted"},
                    "404": {"description": "Not found"},
                },
            },
        },
    },
}


def load_spec(spec_path: str) -> dict:
    """Load an OpenAPI spec from a file path or URL."""
    if spec_path.startswith(("http://", "https://")):
        resp = requests.get(spec_path, timeout=15)
        resp.raise_for_status()
        return resp.json()

    with open(spec_path) as f:
        content = f.read()

    # Try JSON first, then YAML
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return yaml.safe_load(content)


def generate_api_tests(spec: dict) -> str:
    """Send an OpenAPI spec to Claude and return generated test code."""
    client = anthropic.Anthropic()

    # Truncate spec if very large to stay within token limits
    spec_text = json.dumps(spec, indent=2)
    if len(spec_text) > 30000:
        spec_text = spec_text[:30000] + "\n... (truncated)"

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Generate pytest API tests for this OpenAPI spec:\n\n{spec_text}",
            }
        ],
    )

    return message.content[0].text


def main():
    parser = argparse.ArgumentParser(description="Generate API tests from an OpenAPI spec")
    parser.add_argument("--spec", type=str, help="Path or URL to OpenAPI spec (JSON/YAML)")
    parser.add_argument("--output", type=str, help="Write generated tests to this file")
    parser.add_argument("--generate-only", action="store_true", help="Generate tests without running")
    args = parser.parse_args()

    if args.spec:
        print(f"Loading spec from: {args.spec}")
        spec = load_spec(args.spec)
    else:
        print("No spec provided. Using built-in Todo API example.\n")
        spec = EXAMPLE_SPEC

    title = spec.get("info", {}).get("title", "API")
    paths = list(spec.get("paths", {}).keys())
    print(f"API: {title}")
    print(f"Endpoints: {', '.join(paths)}\n")
    print("Generating tests...")

    try:
        generated_code = generate_api_tests(spec)
    except anthropic.AuthenticationError:
        print("Error: Invalid or missing ANTHROPIC_API_KEY.", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, "w") as f:
            f.write(generated_code)
        print(f"Tests written to {args.output}")
    else:
        print("\n--- Generated Tests ---\n")
        print(generated_code)

    if not args.generate_only and not args.output:
        print(textwrap.dedent("""
            To run these tests, save them to a file and use:
                python smart_api_test.py --spec <your-spec> --output test_api.py
                pytest test_api.py -v
        """))


if __name__ == "__main__":
    main()
