from typing import List, Dict

class StorageStrategy:
    def save(self, data: List[Dict[str, any]]):
        raise NotImplementedError("Save method not implemented.")

    def load(self) -> List[Dict[str, any]]:
        raise NotImplementedError("Load method not implemented.")
