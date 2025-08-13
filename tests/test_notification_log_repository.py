import unittest
import os
import json
from repositories.notification_log_repository import NotificationLogRepository

class TestNotificationLogRepository(unittest.TestCase):
    def setUp(self):
        self.test_file = "data/test_notification_log.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.repo = NotificationLogRepository(self.test_file)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load(self):
        entries = [{"id": 1, "notified_on": "2025-08-13", "reason": "Urgent"}]
        self.repo.save_entries(entries)
        loaded_reason = self.repo.last_reason(1)
        self.assertEqual(loaded_reason, "Urgent")

    def test_empty_file(self):
        reason = self.repo.last_reason(99)
        self.assertIsNone(reason)

if __name__ == '__main__':
    unittest.main()