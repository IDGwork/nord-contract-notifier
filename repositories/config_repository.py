import json

class ConfigRepository:
    """Loads rules/priority from config.json."""
    def __init__(self, path="data/config.json"):
        self.path = path

    def read(self):
        with open(self.path, "r") as f:
            return json.load(f)