from __future__ import annotations
from datetime import date
from serializers.contract_serializer import ContractSerializer

class NotifierService:
    """
    Applies RuleEngine to contracts and filters out notifications that are
    not an escalation versus the last notification saved in the log repo.
    """

    def __init__(self, rule_engine, log_repo, priority_order):
        self.rule_engine = rule_engine
        self.log_repo = log_repo
        # lower index means higher priority
        self._rank = {}
        index = 0
        for name in priority_order:
            self._rank[name] = index
            index += 1

    def _escalates(self, previous, current):
        """
        Notify only if there was no previous notification or the new reason
        outranks the previous one (strictly higher priority).
        """
        if previous is None:
            return True
        if self._rank[current] < self._rank[previous]:
            return True
        else:
            return False

    def run(self, contracts, today):
        """
        Evaluate all contracts and return a list of notification dicts.
        Each dict is the serialized contract + {"reason", "notified_on"}.

        NOTE: Persisting to the log should be done by the caller (e.g., CLI)
        using NotificationLogRepository.save_entries(notifications).
        """
        out = []
        for c in contracts:
            reason = self.rule_engine.pick_reason(c, today)
            if reason is None or reason == "":
                continue

            prev = self.log_repo.last_reason(c.id)
            if not self._escalates(prev, reason):
                continue

            obj = ContractSerializer.serialize(c)
            obj["reason"] = reason
            obj["notified_on"] = today.isoformat()
            out.append(obj)

        return out