"""
AI Allure Test Generator — Generate pytest tests with Allure reporting decorators.

Usage:
    export ANTHROPIC_API_KEY="your-key-here"
    python generate_allure_tests.py

    # Pass a feature description directly:
    python generate_allure_tests.py --feature "User can reset their password via email"

    # Save and run with Allure reporting:
    python generate_allure_tests.py --feature "Shopping cart checkout" --output test_checkout.py
    pytest test_checkout.py --alluredir=allure-results
    allure serve allure-results

Requirements:
    pip install anthropic allure-pytest
"""

import argparse
import sys

import anthropic

SYSTEM_PROMPT = """\
You are a senior QA engineer specializing in test reporting. Given a feature \
description, generate a complete, runnable set of pytest test cases with \
Allure reporting decorators. Follow these rules:

- Import allure at the top of the file
- Use @allure.epic(), @allure.feature(), and @allure.story() to organize tests
- Use @allure.severity() to classify test importance (BLOCKER, CRITICAL, NORMAL, MINOR, TRIVIAL)
- Use @allure.title() for human-readable test names
- Use allure.step() context manager inside tests to document key actions
- Use allure.attach() to attach relevant data (request/response bodies, screenshots, etc.)
- Write clear, descriptive test function names using test_ prefix
- Include both happy path and edge case tests
- Use pytest fixtures where appropriate
- Add brief docstrings explaining what each test verifies
- Use assertions with clear failure messages
- Mark tests that need external dependencies with @pytest.mark.skip(reason="...")
- Output ONLY valid Python code, no markdown fences
"""

DEFAULT_FEATURE = """\
User Registration:
- Users can register with email, username, and password
- Email must be a valid format and not already registered
- Username must be 3-20 characters, alphanumeric and underscores only
- Passwords must be at least 8 characters with one uppercase, one lowercase, and one number
- A confirmation email is sent after successful registration
- Users cannot log in until they confirm their email
"""


def generate_allure_tests(feature_description: str) -> str:
    """Send a feature description to Claude and return generated pytest code with Allure decorators."""
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"Generate pytest test cases with full Allure reporting "
                    f"decorators for this feature:\n\n{feature_description}"
                ),
            }
        ],
    )

    return message.content[0].text


def main():
    parser = argparse.ArgumentParser(
        description="Generate pytest tests with Allure reporting from a feature description"
    )
    parser.add_argument("--feature", type=str, help="Feature description (or uses built-in example)")
    parser.add_argument("--output", type=str, help="Write generated tests to this file")
    args = parser.parse_args()

    feature = args.feature or DEFAULT_FEATURE

    print(f"Generating Allure-enabled tests for:\n{feature}\n")
    print("Calling Claude API...")

    try:
        generated_code = generate_allure_tests(feature)
    except anthropic.AuthenticationError:
        print("Error: Invalid or missing ANTHROPIC_API_KEY. Set it in your environment.", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, "w") as f:
            f.write(generated_code)
        print(f"Tests written to {args.output}")
        print(f"\nRun with Allure reporting:")
        print(f"  pytest {args.output} --alluredir=allure-results")
        print(f"  allure serve allure-results")
    else:
        print("\n--- Generated Allure Tests ---\n")
        print(generated_code)


if __name__ == "__main__":
    main()
