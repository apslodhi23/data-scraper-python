from typing import List, Dict
from app.storage.storage_strategy import StorageStrategy


class SQLStorageStrategy(StorageStrategy):
    def __init__(self, database_url: str):
        print("initialization")

    def save(self, data: List[Dict[str, any]]):
       print("Implement SQL Save Function")

    def load(self) -> List[Dict[str, any]]:
       print("Implement SQL Load Function")
        
