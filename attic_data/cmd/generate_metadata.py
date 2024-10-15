import os

from pymongo import MongoClient

from attic_data.core.constants import MONGO_URI
from attic_data.types.sink.mongo import MongoSink
from attic_data.types.sink.pipeline import SinkPipeline

db = MongoClient(MONGO_URI)["attic"]
sink = SinkPipeline([MongoSink(db)])


def _generate_tracking_metadata():
    data = {
        "products": {
            "failed_urls": [],
        }
    }

    sink.dump_to_location_safe("metadata/tracking", data)


def _generate_categories_metadata():
    data = {
        "electronics": 100,
        "fashion": 100,
        "home": 100,
        "beauty": 100,
        "sports": 100,
        "books": 100,
        "toys": 100,
        "automotive": 100,
        "grocery": 100,
        "health": 100,
        "tools": 100,
        "industrial": 100,
        "office": 100,
        "software": 100,
        "gaming": 100,
        "jewelry": 100,
        "musical": 100,
        "camera": 100,
        "mobile": 100,
        "computer": 100,
        "watches": 100,
        "fitness": 100,
        "luggage": 100,
        "personal": 100,
        "decor": 100,
        "lighting": 100,
        "bedding": 100,
        "bathroom": 100,
        "cleaning": 100,
        "party": 100,
        "seasonal": 100,
        "beverages": 100,
        "small": 100,
        "home improvement": 100,
        "building": 100,
        "security": 100,
        "school": 100,
        "hiking": 100,
        "fishing": 100,
        "board": 100,
        "antiques": 100,
        "audio": 100,
    }

    sink.dump_to_location_safe("metadata/categories", data)


def main():
    os.system("clear")

    _generate_tracking_metadata()
    _generate_categories_metadata()
