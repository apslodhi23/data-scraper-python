import json
import os
from typing import List, Dict
from app.storage.storage_strategy import StorageStrategy

class JSONStorageStrategy(StorageStrategy):
    def __init__(self, filename: str):
        self.filename = filename

    def save(self, data: List[Dict[str, any]]):
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load(self) -> List[Dict[str, any]]:
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                return json.load(f)
        return []
