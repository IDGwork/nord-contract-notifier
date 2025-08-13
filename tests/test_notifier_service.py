import unittest
from datetime import date, timedelta
from models.contract import Contract
from services.notifier_service import NotifierService
from services.rule_engine import RuleEngine

class FakeLogRepo:
    def __init__(self, last_reason=None):
        self._last_reason = last_reason
    def last_reason(self, contract_id):
        return self._last_reason

class TestNotifierService(unittest.TestCase):
    def setUp(self):
        rules = [{"reason": "Urgent", "days_to_expiry": 3}]
        priority = ["Urgent"]
        self.engine = RuleEngine(rules, priority)

    def test_escalates_when_no_previous(self):
        log_repo = FakeLogRepo(None)
        service = NotifierService(self.engine, log_repo, ["Urgent"])
        c = Contract(1, "Test", "Owner", "Org", 1000, date.today())
        notifications = service.run([c], date.today())
        self.assertEqual(len(notifications), 1)

    def test_no_escalation(self):
        log_repo = FakeLogRepo("Urgent")
        service = NotifierService(self.engine, log_repo, ["Urgent"])
        c = Contract(1, "Test", "Owner", "Org", 1000, date.today())
        notifications = service.run([c], date.today())
        self.assertEqual(len(notifications), 0)

if __name__ == '__main__':
    unittest.main()