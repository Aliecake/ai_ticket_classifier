import argparse
import json
from collections import Counter
from pathlib import Path

from ticket_classifier.classifier import classify_ticket
from ticket_classifier.models import LabeledTicket


def evaluate(dataset_path: Path, output_path: Path) -> None:
    raw_data = json.loads(dataset_path.read_text(encoding="utf-8"))
    tickets = [
        LabeledTicket.model_validate(item)
        for item in raw_data
    ]

    fields = [
        "category",
        "triage_priority",
        "route",
        "requires_engineering",
    ]

    correct = Counter()
    results = []

    for ticket in tickets:
        prediction = classify_ticket(ticket.text)

        comparisons = {}

        for field in fields:
            expected_value = getattr(ticket.expected, field)
            predicted_value = getattr(prediction, field)
            matches = expected_value == predicted_value

            comparisons[field] = matches

            if matches:
                correct[field] += 1

        results.append(
            {
                "id": ticket.id,
                "text": ticket.text,
                "expected": ticket.expected.model_dump(mode="json"),
                "predicted": prediction.model_dump(mode="json"),
                "matches": comparisons,
            }
        )

    total = len(tickets)

    print(f"\nEvaluated {total} tickets\n")

    for field in fields:
        accuracy = correct[field] / total
        print(f"{field}: {correct[field]}/{total} ({accuracy:.1%})")

    mismatches = [
        result
        for result in results
        if not all(result["matches"].values())
    ]

    print(f"\nTickets with mismatches: {len(mismatches)}/{total}")

    for result in mismatches:
        print(f"\n{result['id']}: {result['text']}")

        for field, matched in result["matches"].items():
            if not matched:
                expected = result["expected"][field]
                predicted = result["predicted"][field]
                print(
                    f"  {field}: expected={expected}, predicted={predicted}"
                )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8",
    )

    print(f"\nResults saved to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        type=Path,
        default=Path("data/labeled_tickets.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/evaluation.json"),
    )
    args = parser.parse_args()

    evaluate(args.dataset, args.output)


if __name__ == "__main__":
    main()