import json
from datetime import date
from repositories.contracts_repository import ContractsRepository
from repositories.config_repository import ConfigRepository
from repositories.notification_log_repository import NotificationLogRepository
from services.rule_engine import RuleEngine
from services.notifier_service import NotifierService


def main(today=None):
    today = today or date.today()

    # Load config & data
    cfg = ConfigRepository().read()
    contracts = ContractsRepository().read_all()
    log_repo = NotificationLogRepository()

    # Set up services
    engine = RuleEngine(cfg["rules"], cfg["priority"])
    notifier = NotifierService(engine, log_repo, cfg["priority"])

    # Generate notifications
    notifications = notifier.run(contracts, today)

    # Prepare data for printing (excluding notified_on)
    filtered_notifications = []
    for n in notifications:
        item = {}
        for k, v in n.items():
            if k != "notified_on":
                item[k] = v
        filtered_notifications.append(item)

    # Print JSON to stdout
    print(json.dumps(filtered_notifications, indent=2))

    # Persist to log
    if len(notifications) > 0:
        log_repo.save_entries(notifications)


if __name__ == "__main__":
    main()