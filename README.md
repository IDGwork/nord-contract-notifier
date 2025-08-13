# nord-contract-notifier

A Python tool that reads software contract data from JSON files, applies configurable rules, and prints notifications for contracts nearing renewal.  
It also writes to a `notification_log.json` so you only get notified again if the reason **escalates** (e.g., from “Upcoming” to “High-Cost” or “Urgent”).

---

## 📦 What it does

- Loads contracts from `data/contracts.json`
- Loads rules & priority from `data/config.json`
- Computes the **single highest-priority** reason per contract
- Prints the notifications to **stdout** (as JSON)
- Persists what was notified into `data/notification_log.json`
- On subsequent runs, **suppresses duplicates** unless the reason escalates

---

## 🗂 Project structure

```
nord-contract-notifier/
├─ cli.py
├─ README.md
├─ requirements.txt
├─ data/
│  ├─ contracts.json
│  ├─ config.json
│  └─ notification_log.json
├─ models/
│  ├─ contract.py
│  └─ notification.py
├─ serializers/
│  ├─ contract_serializer.py
│  └─ notification_serializer.py
├─ repositories/
│  ├─ contracts_repository.py
│  ├─ config_repository.py
│  └─ notification_log_repository.py
├─ services/
│  ├─ rule_engine.py
│  └─ notifier_service.py
└─ tests/
   ├─ test_rule_engine.py
   ├─ test_notifier_service.py
   ├─ test_notification_log_repository.py
   └─ test_integration.py
```

> Note: Keep `__init__.py` files inside `models/`, `serializers/`, `repositories/`, and `services/` so Python treats them as packages.

---

## ✅ Requirements

- Python **3.10+**
- No external libraries required

Install (optional virtualenv recommended):

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows (Powershell)
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

---

## ▶️ Run

From the project root:

```bash
python cli.py
```

It will:
- print notifications to the terminal (JSON array),
- update `data/notification_log.json` with `{ "<id>": { "notified_on": "...", "reason": "..." } }`.

### Running for a specific date (manual way)
For testing with a fixed date, you can temporarily tweak the call in `cli.py`:

```python
if __name__ == "__main__":
    from datetime import date
    main(today=date(2025, 8, 13))  # <- choose your test date
```

Then run:

```bash
python cli.py
```

Switch it back to `main()` when done.

---

## 🧪 Tests

Uses Python’s built-in `unittest`. From the project root:

```bash
python -m unittest discover tests
```

You should see output similar to:

```
........
----------------------------------------------------------------------
Ran 8 tests in 0.00Xs

OK
```

If Python can’t find the packages (e.g., `ModuleNotFoundError: services`), make sure you have these:

- `services/__init__.py`
- `repositories/__init__.py`
- `models/__init__.py`
- `serializers/__init__.py`

and you’re running tests **from the project root**.

---

## ⚙️ Config format

`data/config.json`:

```json
{
  "rules": [
    { "reason": "Urgent", "days_to_expiry": 3 },
    { "reason": "High-Cost", "days_to_expiry": 30, "min_annual_cost": 10000 },
    { "reason": "Upcoming", "days_to_expiry": 14 }
  ],
  "priority": ["Urgent", "High-Cost", "Upcoming"]
}
```

- **rules**: a list of match conditions. A rule fires if `days_to_expiry` is met; optionally also require `min_annual_cost`.
- **priority**: lower index = higher priority. If multiple rules match, the one with highest priority wins.

---

## 📝 Data files

- `data/contracts.json` — input contracts
- `data/config.json` — rules & priority
- `data/notification_log.json` — auto-maintained history used to suppress repeats unless the reason escalates

---

## 💡 Troubleshooting

- **No output?** Check that `data/contracts.json` has records with renewal dates close enough to your run date to hit any rule.
- **Duplicate notifications?** The tool only suppresses if the reason stays the same or downgrades. If it escalates (e.g., Upcoming → Urgent), it will notify again.
- **Tests can’t import modules?** Ensure you run from the project root and have `__init__.py` files in all package directories.

---

## 📄 License

For assessment/demo purposes.
