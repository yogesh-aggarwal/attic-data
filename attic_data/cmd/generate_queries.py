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
        # SinkPipeline([JSONSink("./data")]),
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
    categories = db["metadata"].find_one({"_id": "categories"})
    if categories is None:
        raise ValueError("Categories metadata not found in the database")
    del categories["_id"]

    _generate_queries_for_categories(categories)


def main():
    os.system("clear")

    generate_queries()
