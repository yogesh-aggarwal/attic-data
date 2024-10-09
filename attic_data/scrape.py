import os
import random
import time
import logging

import requests
import bs4

from attic_data.core.utils import cd, prepare_headers

# from selenium.webdriver.common.by import By
# from undetected_chromedriver import Chrome
# driver = Chrome(use_subprocess=False)

logging.basicConfig(filename="log.log", level=logging.INFO)

logger = logging.getLogger(__name__)


def fetch_max_pages_for_query(query: str):
    url = f"https://www.amazon.in/s?k={query}"
    res = requests.get(url, headers=prepare_headers())

    soup = bs4.BeautifulSoup(res.text, "html.parser")

    max_pages = soup.select(".s-pagination-item.s-pagination-disabled")
    if not max_pages:
        return 1
    max_pages = max_pages[-1]
    if max_pages is None:
        return 1
    max_pages = int(max_pages.get_text())

    return max_pages


def fetch_urls(query: str, page: int) -> list[str]:
    url = f"https://www.amazon.in/s?k={query}&page={page}&ref=nb_sb_noss_2"
    res = requests.get(url, headers=prepare_headers())

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    links = soup.select(
        ".a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal"
    )

    urls: set[str] = set()
    for link in links:
        url = link.get("href")
        urls.add(f"https://www.amazon.in{url}")

    return list(urls)


def fetch_all_pages_for_query(query: str):
    urls = []

    max_pages = fetch_max_pages_for_query(query)
    logger.info(f"\t✅ Found {max_pages} pages")

    for page in range(1, max_pages + 1):
        attempts = 3
        while attempts:
            attempts -= 1
            page_urls = fetch_urls(query, page)
            if page_urls:
                urls.extend(page_urls)
                break

        logger.info(f"\t\t✅ Found {len(page_urls)} URLs on page {page}")
    logger.info(f"\t✅ Found {len(urls)} URLs")

    return urls


cd("data")

with open("queries.txt") as f:
    queries = sorted(f.read().strip().split("\n"))
    queries = queries[1:10]

cd("output")

for i, query in enumerate(queries):
    logger.info(f"Fetching URLs for query {i + 1}/{len(queries)}: {query}")
    urls = fetch_all_pages_for_query(query)
    with open(f"{query}.txt", "w") as f:
        f.write("\n".join(urls))

    sleep_time = random.uniform(3, 5)
    logger.info(f"\tSleeping for {sleep_time} seconds")
    time.sleep(sleep_time)


def main():
    pass
