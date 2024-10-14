import os

import ollama
from pymongo import MongoClient

from attic_data.core.constants import MONGO_URI
from attic_data.core.logging import logger
from attic_data.types.sink.json import JSONSink
from attic_data.types.sink.mongo import MongoSink
from attic_data.types.sink.pipeline import SinkPipeline

db = MongoClient(MONGO_URI)["attic"]
sink = SinkPipeline(
    [
        # Database sinks
        SinkPipeline([MongoSink(db)]),
        # File system sinks
        SinkPipeline([JSONSink("./data/queries")]),
    ]
)


def _generate_queries_for_description(description: str) -> list[str]:
    stream = ollama.chat(
        "llama3.2:1b",
        [
            {
                "role": "user",
                "content": f"Generate {description} in the following format:\n\nQUERY: <query>. EACH LINE OF THE RESPONSE SHOULD START WITH 'QUERY:' AND IS A SINGLE QUERY. DON'T USE ANY NUMBERING OR QUOTES",
            },
        ],
        options={"temperature": 0},
        stream=True,
    )

    response = ""
    for chunk in stream:
        content = chunk["message"]["content"]
        response += content
        # print(content, end="")

    lines = response.split("\n")
    lines = map(lambda x: x.strip(), lines)
    lines = filter(lambda x: "QUERY:" in x, lines)
    lines = map(lambda x: x[x.index("QUERY:") + len("QUERY:") :].strip(), lines)

    return list(lines)


def _generate_queries_for_categories(categories: dict[str, int]) -> None:
    for category, count in categories.items():
        logger.info(f"🔍 Generating {count} queries for category: {category}")
        queries = _generate_queries_for_description(
            f"{count} search queries for various {category} products that a user might search for on the search bar of an ecommerce website like Amazon. Make sure that the queries are diverse and cover a wide range of products and MUST RESULT IN PRODUCTS ON AMAZON'S WEBSITE."
        )

        sink.dump_to_location_safe(
            f"queries/{category}", {"category": category, "queries": queries}
        )

        logger.info(f"📦 {count} queries for {category} dumped")


def generate_queries():
    categories = {
        "electronics": 100,
        "clothing": 100,
        "home appliances": 100,
        "books": 100,
        "furniture": 100,
        "beauty products": 100,
        "sports equipment": 100,
        "kitchen appliances": 100,
        "toys": 100,
        "stationery": 100,
        "footwear": 100,
        "jewelry": 100,
        "automotive": 100,
        "pet supplies": 100,
        "office supplies": 100,
        "outdoor gear": 100,
        "health and wellness": 100,
        "gardening tools": 100,
        "baby products": 100,
        "grocery and gourmet": 100,
        "musical instruments": 100,
        "art and craft supplies": 100,
        "camera and photography": 100,
        "mobile phones and accessories": 100,
        "computer hardware": 100,
        "software": 100,
        "gaming": 100,
        "watches": 100,
        "fitness and exercise equipment": 100,
        "luggage and travel gear": 100,
        "personal care": 100,
        "home decor": 100,
        "lighting": 100,
        "bedding and linens": 100,
        "bathroom accessories": 100,
        "cleaning supplies": 100,
        "party supplies": 100,
        "seasonal decor": 100,
        "craft beverages": 100,
        "small home appliances": 100,
        "home improvement": 100,
        "building materials": 100,
        "security systems": 100,
        "industrial supplies": 100,
        "school uniforms": 100,
        "hiking and camping equipment": 100,
        "fishing gear": 100,
        "board games and puzzles": 100,
        "antiques and collectibles": 100,
        "audio and home theater": 100,
    }

    _generate_queries_for_categories(categories)


def main():
    os.system("clear")

    generate_queries()
