from __future__ import annotations
from datetime import date

class RuleEngine:
    """
    Evaluates config rules and returns the single highest-priority reason
    for a given contract (or None if no rule matches).

    Config example:
    rules = [
        {"reason": "Urgent", "days_to_expiry": 3},
        {"reason": "High-Cost", "days_to_expiry": 30, "min_annual_cost": 10000},
        {"reason": "Upcoming", "days_to_expiry": 14}
    ]
    priority = ["Urgent", "High-Cost", "Upcoming"]  # index order = priority
    """

    def __init__(self, rules, priority):
        self.rules = rules
        # lower index means higher priority
        self._rank = {}
        index = 0
        for name in priority:
            self._rank[name] = index
            index += 1

    def pick_reason(self, contract, today):
        """
        Return highest-priority matching reason for the contract.
        """
        days = (contract.renewal_date - today).days
        matches = []

        for r in self.rules:
            if days <= r["days_to_expiry"]:
                if "min_annual_cost" in r:
                    if contract.annual_cost_eur < r["min_annual_cost"]:
                        continue
                matches.append(r["reason"])

        if len(matches) == 0:
            return None

        # choose the one with best (lowest) rank; unknown reasons sink to bottom
        best_name = None
        best_rank = 10**9
        for name in matches:
            rank = self._rank.get(name, 10**9)
            if best_name is None or rank < best_rank:
                best_name = name
                best_rank = rank

        return best_name