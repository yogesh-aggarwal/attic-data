from typing import Any, override

from pymongo.database import Database

from . import Sink


class MongoSink(Sink):
    db: Database

    def __init__(self, db: Database):
        super().__init__()
        self.db = db

    @override
    def dump_to_location(self, doc_path: str, data: dict[str, Any]):
        collection, doc_id = doc_path.split("/")
        self.db[collection].replace_one({"_id": doc_id}, data, upsert=True)
