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

    with cd("data"):
        _generate_queries_for_categories(categories)
        _articulate_queries_in_one_file()


def main():
    os.system("clear")

    with cd("data"):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    generate_and_articulate_queries()
