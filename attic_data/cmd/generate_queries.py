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
        SinkPipeline([JSONSink("./data")]),
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
    lines = map(lambda x: x.lower().replace('"', ""), lines)

    return list(lines)


def _generate_queries_for_categories(categories: dict[str, int]) -> None:
    for category, count in categories.items():
        logger.info(f"🔍 Generating {count} queries for category: {category}")
        queries = _generate_queries_for_description(
            f"I want you to generate {count} search queries for various {category} products that a user might search for on the search bar of an ecommerce website like Amazon. Make sure that the queries are diverse and cover a wide range of products and MUST RESULT IN PRODUCTS ON AMAZON'S WEBSITE. The queries must be of count {count}."
        )

        sink.dump_to_location_safe(
            f"queries/{category}", {"category": category, "queries": queries}
        )

        logger.info(f"📦 {count} queries for {category} dumped")


def generate_queries():
    categories = {
        "electronics": 89,
        "clothing": 89,
        "home appliances": 89,
        "books": 89,
        "furniture": 89,
        "beauty products": 89,
        "sports equipment": 89,
        "kitchen appliances": 89,
        "toys": 89,
        "stationery": 89,
        "footwear": 89,
        "jewelry": 89,
        "automotive": 89,
        "pet supplies": 89,
        "office supplies": 89,
        "outdoor gear": 89,
        "health and wellness": 89,
        "gardening tools": 89,
        "baby products": 89,
        "grocery and gourmet": 89,
        "musical instruments": 89,
        "art and craft supplies": 89,
        "camera and photography": 89,
        "mobile phones and accessories": 89,
        "computer hardware": 89,
        "software": 89,
        "gaming": 89,
        "watches": 89,
        "fitness and exercise equipment": 89,
        "luggage and travel gear": 89,
        "personal care": 89,
        "home decor": 89,
        "lighting": 89,
        "bedding and linens": 89,
        "bathroom accessories": 89,
        "cleaning supplies": 89,
        "party supplies": 89,
        "seasonal decor": 89,
        "craft beverages": 89,
        "small home appliances": 89,
        "home improvement": 89,
        "building materials": 89,
        "security systems": 89,
        "industrial supplies": 89,
        "school uniforms": 89,
        "hiking and camping equipment": 89,
        "fishing gear": 89,
        "board games and puzzles": 89,
        "antiques and collectibles": 89,
        "audio and home theater": 89,
    }

    _generate_queries_for_categories(categories)


def main():
    os.system("clear")

    generate_queries()
