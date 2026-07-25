"""AI support ticket classifier."""

from ticket_classifier.classifier import classify_ticket
from ticket_classifier.models import TicketClassification

__all__ = ["TicketClassification", "classify_ticket"]
