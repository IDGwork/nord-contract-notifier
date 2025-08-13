import unittest
from datetime import date, timedelta
from models.contract import Contract
from services.rule_engine import RuleEngine
from services.notifier_service import NotifierService

class FakeLogRepo:
    def __init__(self):
        self.saved = []
    def last_reason(self, contract_id):
        return None
    def save_entries(self, entries):
        self.saved.extend(entries)

class TestIntegration(unittest.TestCase):
    def test_full_flow(self):
        rules = [
            {"reason": "Urgent", "days_to_expiry": 3},
            {"reason": "High-Cost", "days_to_expiry": 30, "min_annual_cost": 10000},
            {"reason": "Upcoming", "days_to_expiry": 14}
        ]
        priority = ["Urgent", "High-Cost", "Upcoming"]

        contracts = [
            Contract(1, "SoftA", "Owner", "Org", 12000, date.today() + timedelta(days=1)),
            Contract(2, "SoftB", "Owner", "Org", 5000, date.today() + timedelta(days=10))
        ]

        engine = RuleEngine(rules, priority)
        log_repo = FakeLogRepo()
        notifier = NotifierService(engine, log_repo, priority)
        notifications = notifier.run(contracts, date.today())

        self.assertEqual(len(notifications), 2)
        self.assertEqual(notifications[0]["reason"], "Urgent")

if __name__ == '__main__':
    unittest.main()