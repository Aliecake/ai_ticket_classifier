# AI Support Ticket Classifier

A small AI engineering project that classifies customer-support tickets using
OpenAI Structured Outputs and Pydantic.

This repository begins as a focused Lesson 3 project:

- define a typed output schema;
- send an unstructured ticket to an LLM;
- receive a validated Python object;
- keep model access separate from the command-line interface;
- test deterministic application behavior without making API calls.

## Example

Input:

```text
I was charged twice for my subscription. Please refund the duplicate charge.
```

Structured output:

```json
{
  "category": "billing",
  "priority": "high",
  "route": "support",
  "requires_engineering": false,
  "summary": "Customer reports a duplicate subscription charge.",
  "confidence": 0.98
}
```

## Requirements

- Python 3.10+
- An OpenAI API key

## Setup

Clone the repository and create a virtual environment:

### PowerShell

```powershell
git clone <YOUR_REPOSITORY_URL>
cd ai-support-ticket-classifier

py -m venv .venv
.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Copy the environment template:

```powershell
Copy-Item .env.example .env
```

Add your API key to `.env`:

```text
OPENAI_API_KEY=your-key-here
```

Never commit `.env`.

## Run

Classify a ticket passed on the command line:

```powershell
python -m ticket_classifier.cli "I was charged twice for my subscription."
```

Or omit the ticket and enter it interactively:

```powershell
python -m ticket_classifier.cli
```

Choose a different supported model by setting `OPENAI_MODEL` in `.env`.

## Test

```powershell
pytest
```

The initial tests do not call OpenAI, so they are fast and do not cost money.

## Project structure

```text
src/ticket_classifier/
├── classifier.py   # OpenAI integration
├── cli.py          # command-line interface
├── config.py       # environment configuration
└── models.py       # structured-output schema
tests/
└── test_models.py
```

## Current scope

Version 0.1 deliberately classifies one ticket at a time. It does not yet:

- classify batches;
- calculate accuracy against labeled examples;
- retrieve documentation;
- call tools;
- create autonomous agents.

Those are later milestones. Keeping the first version narrow makes its behavior
easy to understand and evaluate.

## Learning goals

After completing this version, you should be able to explain:

1. Why a Pydantic model is preferable to asking the model to "return JSON."
2. Which fields should use enums rather than unrestricted strings.
3. Which validation belongs in Python versus the prompt.
4. Why confidence is the model's estimate, not proof of correctness.
5. Why tests should avoid real API calls unless they are explicit integration tests.

## Suggested next milestones

1. Add 20 labeled sample tickets.
2. Add a batch classifier that reads JSONL.
3. Compare predictions with expected labels.
4. Produce accuracy and confusion reports.
5. Add tool calling only after classification is measurable.
