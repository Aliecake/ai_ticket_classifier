from enum import Enum

from pydantic import BaseModel, Field

#Enums
class TicketCategory(str, Enum):
    BILLING = "billing"
    ACCOUNT_ACCESS = "account_access"
    BUG = "bug"
    FEATURE_REQUEST = "feature_request"
    HOW_TO = "how_to"
    OTHER = "other"


class TriagePriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


TicketPriority = TriagePriority


class TicketRoute(str, Enum):
    SUPPORT = "support"
    ENGINEERING = "engineering"
    PRODUCT = "product"
    SECURITY = "security"

# models

class ExpectedClassification(BaseModel):
    category: TicketCategory
    triage_priority: TriagePriority
    route: TicketRoute
    requires_engineering: bool


class LabeledTicket(BaseModel):
    id: str
    text: str
    expected: ExpectedClassification

class TicketClassification(BaseModel):
    """Validated output returned by the language model."""

    category: TicketCategory = Field(
        description="The primary topic of the customer's request."
    )
    triage_priority: TriagePriority = Field(
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
