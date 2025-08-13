import json
import os

class NotificationLogRepository:
    """
    Reads/writes notification_log.json as a simple
    { "<contract_id>": {"notified_on": "...", "reason": "..."} } map.
    """
    def __init__(self, path="data/notification_log.json"):
        self.path = path

    def _load(self):
        if not os.path.exists(self.path):
            return {}
        with open(self.path, "r") as f:
            data = f.read().strip()
            if data:
                return json.loads(data)
            else:
                return {}

    def last_reason(self, contract_id):
        loaded_data = self._load()
        if str(contract_id) in loaded_data:
            entry = loaded_data[str(contract_id)]
            if "reason" in entry:
                return entry["reason"]
        return None

    def save_entries(self, entries):
        data = self._load()
        for e in entries:
            # expects each entry to include: id, notified_on, reason
            data[str(e["id"])] = {
                "notified_on": e["notified_on"],
                "reason": e["reason"],
            }
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)