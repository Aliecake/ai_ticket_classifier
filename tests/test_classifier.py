import ticket_classifier.classifier as classifier_module
from ticket_classifier.config import Settings
from ticket_classifier.models import TicketCategory, TicketClassification, TicketPriority, TicketRoute


def test_classify_ticket_passes_timeout_and_retries_to_openai_client(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class FakeResponses:
        def parse(self, **kwargs):
            return type("Response", (), {"output_parsed": TicketClassification(
                category=TicketCategory.BILLING,
                triage_priority=TicketPriority.HIGH,
                route=TicketRoute.SUPPORT,
                requires_engineering=False,
                summary="Billing issue",
                confidence=0.9,
            )})()

    class FakeClient:
        def __init__(self, **kwargs):
            captured.update(kwargs)
            self.responses = FakeResponses()

    monkeypatch.setattr(classifier_module, "OpenAI", FakeClient)

    settings = Settings(
        openai_api_key="test-key",
        openai_model="gpt-test",
        openai_timeout=45.0,
        openai_max_retries=3,
    )

    result = classifier_module.classify_ticket("Need help with billing", settings=settings)

    assert result.summary == "Billing issue"
    assert captured["timeout"] == 45.0
    assert captured["max_retries"] == 3
