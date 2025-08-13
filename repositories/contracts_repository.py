import json
from serializers.contract_serializer import ContractSerializer

class ContractsRepository:
    """Read-only repository for contracts.json."""
    def __init__(self, path="data/contracts.json"):
        self.path = path

    def read_all(self):
        with open(self.path, "r") as f:
            raw = json.load(f)
        result = []
        for x in raw:
            result.append(ContractSerializer.deserialize(x))
        return result