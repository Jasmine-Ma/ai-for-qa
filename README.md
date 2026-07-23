# AI for QA

A practical learning resource for QA engineers exploring how AI and large language models can enhance test automation workflows.

## What's Inside

Each example is a self-contained Python script demonstrating a real-world use case for AI in QA:

| Example | Description |
|---------|-------------|
| [`examples/ai_test_generator/`](examples/ai_test_generator/) | Generate pytest test cases from a plain-English feature description |
| [`examples/ai_bug_analyzer/`](examples/ai_bug_analyzer/) | Feed stack traces and failure logs to get root cause suggestions |
| [`examples/ai_api_tester/`](examples/ai_api_tester/) | Auto-generate and run API tests from an OpenAPI spec |
| [`examples/ai_test_data/`](examples/ai_test_data/) | Generate realistic, structured test data sets |

The [`archive/`](archive/) directory contains legacy Selenium and API test code from the original repo, preserved for reference.

## Prerequisites

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/) (set as `ANTHROPIC_API_KEY` environment variable)

## Getting Started

```bash
# Clone the repo
git clone https://github.com/Jasmine-Ma/ai-for-qa.git
cd ai-for-qa

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies for a specific example
pip install -r examples/ai_test_generator/requirements.txt

# Set your API key
export ANTHROPIC_API_KEY="your-key-here"

# Run an example
python examples/ai_test_generator/generate_tests.py
```

## Contributing

We'd love your input! See [CONTRIBUTING.md](CONTRIBUTING.md) for how to get involved, or jump straight into [GitHub Discussions](https://github.com/Jasmine-Ma/ai-for-qa/discussions) to ask questions, share ideas, or show what you've built.

## License

This project is provided as-is for educational purposes.
