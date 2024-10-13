import os

import ollama

from attic_data.core.logging import logger
from attic_data.core.utils import cd


OUTPUT_DIR = "queries"


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

        file_path = f"{OUTPUT_DIR}/{category}.txt"
        with open(file_path, "w+") as f:
            f.write("\n".join(queries))

        logger.info(f"📦 {count} queries for {category} dumped to {file_path}")


def _articulate_queries_in_one_file():
    # Get all files in the output directory
    files = []
    for root, _, filenames in os.walk(OUTPUT_DIR):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    # Read all URLs from all files
    all_queries: list[str] = []
    for file in files:
        with open(file, "r") as f:
            all_queries += f.read().strip().split("\n")

    # Remove trailing and leading whitespaces
    queries = map(lambda x: x.strip(), all_queries)
    # Remove duplicates
    queries = list(set(queries))

    with open("queries.txt", "w+") as f:
        f.write("\n".join(queries))

    logger.info(f"📦 {len(queries)} queries dumped to queries.txt")


def generate_and_articulate_queries():
    categories = {
        "electronics": 50,
        "clothing": 50,
        "home appliances": 50,
        "books": 50,
        "furniture": 50,
        "beauty products": 50,
        "sports equipment": 50,
        "kitchen appliances": 50,
        "toys": 50,
        "stationery": 50,
    }

    with cd("data"):
        _generate_queries_for_categories(categories)
        _articulate_queries_in_one_file()


def main():
    os.system("clear")

    with cd("data"):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    generate_and_articulate_queries()
