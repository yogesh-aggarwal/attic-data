import os
import random
import time

import bs4
import requests

from attic_data.core.logging import logger
from attic_data.core.utils import cd, prepare_headers
from attic_data.core.request import make_get_request_with_proxy


OUTPUT_DIR = "product_urls"


def _fetch_max_pages_for_query(query: str):
    url = f"https://www.amazon.in/s?k={query}"
    res = make_get_request_with_proxy(url)
    if res is None:
        return 1

    soup = bs4.BeautifulSoup(res.text, "html.parser")

    max_pages = soup.select(".s-pagination-item.s-pagination-disabled")
    if not max_pages:
        return 1
    max_pages = max_pages[-1]
    if max_pages is None:
        return 1
    max_pages = int(max_pages.get_text())

    return max_pages


def _fetch_urls(query: str, page: int) -> list[str]:
    url = f"https://www.amazon.in/s?k={query}&page={page}&ref=nb_sb_noss_2"
    res = make_get_request_with_proxy(url)
    if res is None:
        return []

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    links = soup.select(
        ".a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal"
    )

    urls: set[str] = set()
    for link in links:
        url = link.get("href")
        urls.add(f"https://www.amazon.in{url}")

    return list(urls)


def _fetch_all_pages_for_query(query: str):
    urls = []

    max_pages = _fetch_max_pages_for_query(query)
    logger.info(f"\t✅ Found {max_pages} pages")

    for page in range(1, max_pages + 1):
        attempts = 3
        while attempts:
            attempts -= 1
            page_urls = _fetch_urls(query, page)
            if page_urls:
                urls.extend(page_urls)
                break

        logger.info(f"\t\t✅ Found {len(page_urls)} URLs on page {page}")
    logger.info(f"\t✅ Found {len(urls)} URLs")

    return urls


def _scrape_product_links_from_queries(queries: list[str]):
    with cd(OUTPUT_DIR):
        for i, query in enumerate(queries):
            logger.info(f"Fetching URLs for query {i + 1}/{len(queries)}: {query}")
            urls = _fetch_all_pages_for_query(query)
            with open(f"{query}.txt", "w+") as f:
                f.write("\n".join(urls))

            sleep_time = random.uniform(3, 5)
            logger.info(f"\tSleeping for {sleep_time} seconds")
            time.sleep(sleep_time)


def _articulate_urls_in_one_file():
    # Get all files in the output directory
    files = []
    for root, _, filenames in os.walk(OUTPUT_DIR):
        for filename in filenames:
            files.append(os.path.join(root, filename))

    # Read all URLs from all files
    all_urls: list[str] = []
    for file in files:
        with open(file, "r") as f:
            all_urls += f.read().strip().split("\n")

    # Remove trailing and leading whitespaces
    urls = map(lambda x: x.strip(), all_urls)
    # Remove invalid URLs
    urls = map(lambda x: x[x.rfind("https://") :], urls)
    # Remove query parameters
    urls = map(lambda x: x.split("?")[0], urls)
    # Remove invalid URLs
    urls = filter(lambda x: x.startswith("https://www.amazon."), urls)
    # Remove duplicates
    urls = list(set(urls))

    with open("urls.txt", "w+") as f:
        f.write("\n".join(urls))

    logger.info(f"📦 {len(urls)} URLs dumped to urls.txt")


def scrape_product_links_from_queries_file(file_path: str):
    with cd("data"):
        with open(file_path) as f:
            queries = sorted(f.read().strip().split("\n"))
        _scrape_product_links_from_queries(queries)
        _articulate_urls_in_one_file()


def main():
    os.system("clear")

    with cd("data"):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    scrape_product_links_from_queries_file("queries.txt")
