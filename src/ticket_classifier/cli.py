import argparse
import json
import sys

import openai
from pydantic import ValidationError

from ticket_classifier.classifier import classify_ticket


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Classify a customer-support ticket using structured AI output."
    )
    parser.add_argument(
        "ticket",
        nargs="?",
        help="Ticket text. When omitted, you will be prompted to enter it.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    ticket = args.ticket or input("Paste a support ticket:\n> ")

    try:
        result = classify_ticket(ticket)
    except ValueError as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    except ValidationError as exc:
        print(f"Validation error: {exc}", file=sys.stderr)
        raise SystemExit(3) from exc
    except openai.OpenAIError as exc:
        print(f"OpenAI API error: {exc}", file=sys.stderr)
        raise SystemExit(4) from exc
    except RuntimeError as exc:
        print(f"Classification error: {exc}", file=sys.stderr)
        raise SystemExit(5) from exc

    print(json.dumps(result.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    main()
