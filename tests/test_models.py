import pytest
from pydantic import ValidationError

from ticket_classifier.models import (
    TicketCategory,
    TicketClassification,
    TicketPriority,
    TicketRoute,
)


def test_valid_classification() -> None:
    classification = TicketClassification(
        category=TicketCategory.BILLING,
        priority=TicketPriority.HIGH,
        route=TicketRoute.SUPPORT,
        requires_engineering=False,
        summary="Customer reports a duplicate subscription charge.",
        confidence=0.95,
    )

    assert classification.category is TicketCategory.BILLING
    assert classification.confidence == 0.95


@pytest.mark.parametrize("confidence", [-0.01, 1.01])
def test_confidence_must_be_between_zero_and_one(confidence: float) -> None:
    with pytest.raises(ValidationError):
        TicketClassification(
            category=TicketCategory.BUG,
            priority=TicketPriority.MEDIUM,
            route=TicketRoute.ENGINEERING,
            requires_engineering=True,
            summary="Customer reports a reproducible application error.",
            confidence=confidence,
        )


def test_summary_cannot_be_empty() -> None:
    with pytest.raises(ValidationError):
        TicketClassification(
            category=TicketCategory.OTHER,
            priority=TicketPriority.LOW,
            route=TicketRoute.SUPPORT,
            requires_engineering=False,
            summary="",
            confidence=0.5,
        )
