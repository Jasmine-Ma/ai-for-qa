"""
AI Test Generator — Generate pytest test cases from a feature description.

Usage:
    export ANTHROPIC_API_KEY="your-key-here"
    python generate_tests.py

    # Or pass a feature description directly:
    python generate_tests.py --feature "User can reset their password via email"

    # Save the generated tests to a file:
    python generate_tests.py --feature "Shopping cart checkout" --output test_checkout.py

Requirements:
    pip install anthropic
"""

import argparse
import sys

import anthropic

SYSTEM_PROMPT = """\
You are a senior QA engineer. Given a feature description, generate a complete, \
runnable set of pytest test cases. Follow these rules:

- Write clear, descriptive test function names using test_ prefix
- Include both happy path and edge case tests
- Use pytest fixtures where appropriate
- Add brief docstrings explaining what each test verifies
- Use assertions with clear failure messages
- Mark tests that need external dependencies with @pytest.mark.skip(reason="...")
- Output ONLY valid Python code, no markdown fences
"""

DEFAULT_FEATURE = """\
User Login:
- Users can log in with email and password
- Failed login after 5 attempts locks the account for 30 minutes
- Passwords must be at least 8 characters with one uppercase and one number
- Users can request a password reset link via email
- Reset links expire after 1 hour
"""


def generate_tests(feature_description: str) -> str:
    """Send a feature description to Claude and return generated pytest code."""
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Generate pytest test cases for this feature:\n\n{feature_description}",
            }
        ],
    )

    return message.content[0].text


def main():
    parser = argparse.ArgumentParser(description="Generate pytest tests from a feature description")
    parser.add_argument("--feature", type=str, help="Feature description (or uses built-in example)")
    parser.add_argument("--output", type=str, help="Write generated tests to this file")
    args = parser.parse_args()

    feature = args.feature or DEFAULT_FEATURE

    print(f"Generating tests for:\n{feature}\n")
    print("Calling Claude API...")

    try:
        generated_code = generate_tests(feature)
    except anthropic.AuthenticationError:
        print("Error: Invalid or missing ANTHROPIC_API_KEY. Set it in your environment.", file=sys.stderr)
        sys.exit(1)

    if args.output:
        with open(args.output, "w") as f:
            f.write(generated_code)
        print(f"Tests written to {args.output}")
    else:
        print("\n--- Generated Tests ---\n")
        print(generated_code)


if __name__ == "__main__":
    main()
