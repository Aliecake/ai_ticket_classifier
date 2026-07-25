from openai import OpenAI

from ticket_classifier.config import Settings
from ticket_classifier.models import TicketClassification


CLASSIFIER_INSTRUCTIONS = """
You classify customer-support tickets for a software company.

Rules:
- Base the classification only on information in the ticket.
- Do not invent customer impact, outages, security incidents, or technical causes.
- Use urgent only for credible security risk, widespread outage, data loss,
  or a customer-blocking emergency with substantial impact.
- Route feature requests to product.
- Route likely code defects to engineering.
- Route ordinary billing, access, and how-to requests to support.
- Keep the summary factual and concise.
- Confidence is an estimate, not a claim of certainty.
""".strip()


def classify_ticket(
    ticket_text: str,
    *,
    client: OpenAI | None = None,
    settings: Settings | None = None,
) -> TicketClassification:
    """Classify one support ticket into a validated Pydantic model."""

    cleaned_ticket = ticket_text.strip()
    if not cleaned_ticket:
        raise ValueError("Ticket text cannot be empty.")

    resolved_settings = settings or Settings()
    resolved_client = client or OpenAI(api_key=resolved_settings.openai_api_key)

    response = resolved_client.responses.parse(
        model=resolved_settings.openai_model,
        instructions=CLASSIFIER_INSTRUCTIONS,
        input=cleaned_ticket,
        text_format=TicketClassification,
    )

    classification = response.output_parsed
    if classification is None:
        raise RuntimeError("The model did not return a parsed ticket classification.")

    return classification
