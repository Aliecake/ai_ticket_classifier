from enum import Enum

from pydantic import BaseModel, Field


class TicketCategory(str, Enum):
    BILLING = "billing"
    ACCOUNT_ACCESS = "account_access"
    BUG = "bug"
    FEATURE_REQUEST = "feature_request"
    HOW_TO = "how_to"
    OTHER = "other"


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TicketRoute(str, Enum):
    SUPPORT = "support"
    ENGINEERING = "engineering"
    PRODUCT = "product"
    SECURITY = "security"


class TicketClassification(BaseModel):
    """Validated output returned by the language model."""

    category: TicketCategory = Field(
        description="The primary topic of the customer's request."
    )
    triage_priority: TicketPriority = Field(
        description="Operational triaging priority based on impact, urgency, and scope."
    )
    route: TicketRoute = Field(
        description="The team best suited to own the next action."
    )
    requires_engineering: bool = Field(
        description="Whether resolving the ticket probably requires a code or infrastructure change."
    )
    summary: str = Field(
        min_length=1,
        max_length=240,
        description="A concise, factual summary of the customer's problem."
    )
    confidence: float = Field(
        ge=0.0,
        le=1.0,
        description="The model's estimated confidence in the classification."
    )
