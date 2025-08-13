import unittest
from datetime import date, timedelta
from models.contract import Contract
from services.rule_engine import RuleEngine

class TestRuleEngine(unittest.TestCase):
    def setUp(self):
        self.rules = [
            {"reason": "Urgent", "days_to_expiry": 3},
            {"reason": "High-Cost", "days_to_expiry": 30, "min_annual_cost": 10000},
            {"reason": "Upcoming", "days_to_expiry": 14}
        ]
        self.priority = ["Urgent", "High-Cost", "Upcoming"]
        self.engine = RuleEngine(self.rules, self.priority)

    def test_urgent_reason(self):
        c = Contract(1, "TestSoft", "Owner", "Org", 5000, date.today() + timedelta(days=2))
        reason = self.engine.pick_reason(c, date.today())
        self.assertEqual(reason, "Urgent")

    def test_high_cost_reason(self):
        c = Contract(2, "CostlySoft", "Owner", "Org", 20000, date.today() + timedelta(days=20))
        reason = self.engine.pick_reason(c, date.today())
        self.assertEqual(reason, "High-Cost")

    def test_no_match(self):
        c = Contract(3, "FarSoft", "Owner", "Org", 2000, date.today() + timedelta(days=100))
        reason = self.engine.pick_reason(c, date.today())
        self.assertIsNone(reason)

if __name__ == '__main__':
    unittest.main()