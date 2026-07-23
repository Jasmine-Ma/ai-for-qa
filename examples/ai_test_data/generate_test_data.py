"""
AI Test Data Generator — Use AI to create realistic, structured test data sets.

Usage:
    export ANTHROPIC_API_KEY="your-key-here"

    # Generate test data using built-in example schema:
    python generate_test_data.py

    # Specify a schema and how many records:
    python generate_test_data.py --schema '{"name": "string", "age": "int", "email": "email"}' --count 10

    # Save as JSON:
    python generate_test_data.py --count 20 --output test_users.json

    # Specify a domain for more realistic data:
    python generate_test_data.py --domain "e-commerce orders" --count 5

Requirements:
    pip install anthropic
"""

import argparse
import json
import sys

import anthropic

SYSTEM_PROMPT = """\
You are a test data generation expert. Given a data schema or domain description, \
generate realistic test data as a JSON array.

Follow these rules:
- Output ONLY a valid JSON array, no explanations or markdown
- Use realistic but fake data (no real PII)
- Include edge cases naturally: empty strings, boundary values, special characters, \
unicode, very long values, null for optional fields
- Vary the data — don't repeat patterns
- Emails should use @example.com (RFC 2606 reserved domain)
- Phone numbers should use 555- prefix (reserved for fiction)
- Dates should use ISO 8601 format
- Distribute values across reasonable ranges
"""

EXAMPLE_SCHEMA = {
    "user_id": "uuid",
    "name": "string (full name)",
    "email": "email",
    "age": "integer (18-90)",
    "subscription": "enum: free, pro, enterprise",
    "signup_date": "ISO date",
    "is_active": "boolean",
    "address": {
        "street": "string",
        "city": "string",
        "state": "US state code",
        "zip": "US zip code",
    },
}


def generate_test_data(schema: str, count: int, domain: str | None = None) -> str:
    """Send a schema to Claude and return generated test data as JSON."""
    client = anthropic.Anthropic()

    prompt_parts = [f"Generate {count} records of test data."]
    if domain:
        prompt_parts.append(f"Domain: {domain}")
    prompt_parts.append(f"Schema:\n{schema}")

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": "\n\n".join(prompt_parts),
            }
        ],
    )

    return message.content[0].text


def main():
    parser = argparse.ArgumentParser(description="Generate realistic test data with AI")
    parser.add_argument("--schema", type=str, help="JSON schema or description of fields")
    parser.add_argument("--domain", type=str, help="Domain context (e.g., 'healthcare patients')")
    parser.add_argument("--count", type=int, default=5, help="Number of records to generate (default: 5)")
    parser.add_argument("--output", type=str, help="Write output to a JSON file")
    args = parser.parse_args()

    if args.schema:
        schema_text = args.schema
    else:
        print("No schema provided. Using built-in user profile example.\n")
        schema_text = json.dumps(EXAMPLE_SCHEMA, indent=2)

    print(f"Generating {args.count} records...")

    try:
        raw_output = generate_test_data(schema_text, args.count, args.domain)
    except anthropic.AuthenticationError:
        print("Error: Invalid or missing ANTHROPIC_API_KEY.", file=sys.stderr)
        sys.exit(1)

    # Validate that the output is valid JSON
    try:
        data = json.loads(raw_output)
        formatted = json.dumps(data, indent=2)
    except json.JSONDecodeError:
        print("Warning: AI output was not valid JSON. Showing raw output.\n", file=sys.stderr)
        formatted = raw_output

    if args.output:
        with open(args.output, "w") as f:
            f.write(formatted)
        print(f"{len(data) if isinstance(data, list) else '?'} records written to {args.output}")
    else:
        print("\n--- Generated Test Data ---\n")
        print(formatted)


if __name__ == "__main__":
    main()
