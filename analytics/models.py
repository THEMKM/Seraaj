from dataclasses import dataclass
from datetime import datetime


@dataclass
class VolunteerEvent:
    """Represents a volunteering event for analytics."""

    volunteer_id: str
    organization_id: str
    opportunity_id: str
    hours: float
    timestamp: datetime
