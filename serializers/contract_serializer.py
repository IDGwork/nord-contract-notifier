from models.contract import Contract
from datetime import date

class ContractSerializer:
    @staticmethod
    def deserialize(d: dict) -> Contract:
        return Contract(
            id=d["id"],
            software_name=d["software_name"],
            owner=d["owner"],
            organization=d["organization"],
            annual_cost_eur=float(d["annual_cost_eur"]),
            renewal_date=date.fromisoformat(d["renewal_date"]),
        )

    @staticmethod
    def serialize(c: Contract) -> dict:
        return {
            "id": c.id,
            "software_name": c.software_name,
            "owner": c.owner,
            "organization": c.organization,
            "annual_cost_eur": c.annual_cost_eur,
            "renewal_date": c.renewal_date.isoformat(),
        }