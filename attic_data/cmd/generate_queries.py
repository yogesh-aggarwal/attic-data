import os
import json

import ollama

from attic_data.core.logging import logger
from attic_data.core.utils import cd


OUTPUT_FILE = "queries_gen.txt"


def _generate_queries(description: str) -> list[str]:
    stream = ollama.chat(
        "llama3.2:1b",
        [
            {
                "role": "user",
                "content": f"Generate {description} in the following format:\n\nQUERY: <query>",
            },
        ],
        options={"temperature": 0},
        stream=True,
    )

    response = ""
    for chunk in stream:
        content = chunk["message"]["content"]
        response += content
        print(content, end="")

    with open(OUTPUT_FILE + ".txt", "w+") as f:
        f.write(response)

    lines = response.split("\n")
    lines = map(lambda x: x.strip(), lines)
    lines = filter(lambda x: "QUERY:" in x, lines)
    lines = map(lambda x: x[x.index("QUERY:") + len("QUERY:") :].strip(), lines)

    return list(lines)


def generate_and_dump_queries():
    logger.info("🦙 Generating queries")

    with cd("data"):
        queries = _generate_queries(
            "1000 search queries for various different products that a user might search for on the search bar of an ecommerce website like Amazon. Make sure that the queries are diverse and cover a wide range of products and MUST RESULT IN PRODUCTS ON AMAZON'S WEBSITE."
        )
        with open(OUTPUT_FILE, "w+") as f:
            f.write("\n".join(queries))

    logger.info(f"📦 Queries generated and dumped to data/{OUTPUT_FILE}")


def main():
    os.system("clear")
    generate_and_dump_queries()
