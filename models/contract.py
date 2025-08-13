from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class Contract:
    id: int
    software_name: str
    owner: str
    organization: str
    annual_cost_eur: float
    renewal_date: date
