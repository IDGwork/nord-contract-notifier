from models.notification import Notification
from datetime import date

class NotificationSerializer:
    @staticmethod
    def deserialize(d: dict) -> Notification:
        return Notification(
            id=d["id"],
            software_name=d["software_name"],
            owner=d["owner"],
            organization=d["organization"],
            annual_cost_eur=float(d["annual_cost_eur"]),
            renewal_date=date.fromisoformat(d["renewal_date"]),
            reason=d["reason"],
            notified_on=date.fromisoformat(d["notified_on"]),
        )

    @staticmethod
    def serialize(n: Notification) -> dict:
        return {
            "id": n.id,
            "software_name": n.software_name,
            "owner": n.owner,
            "organization": n.organization,
            "annual_cost_eur": n.annual_cost_eur,
            "renewal_date": n.renewal_date.isoformat(),
            "reason": n.reason,
            "notified_on": n.notified_on.isoformat(),
        }