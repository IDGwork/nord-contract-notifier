from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class Notification:
    id: int
    software_name: str
    owner: str
    organization: str
    annual_cost_eur: float
    renewal_date: date
    reason: str
    notified_on: date