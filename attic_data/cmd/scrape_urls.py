import os
from concurrent.futures import ThreadPoolExecutor

import bs4
from pymongo import MongoClient

from attic_data.core.constants import MONGO_URI, THREAD_POOL_MAX_WORKERS
from attic_data.core.logging import logger
from attic_data.core.request import make_get_request_with_proxy
from attic_data.core.utils import with_retry
from attic_data.types.sink.json import JSONSink
from attic_data.types.sink.mongo import MongoSink
from attic_data.types.sink.pipeline import SinkPipeline

db = MongoClient(MONGO_URI)["attic"]
sink = SinkPipeline(
    [
        # Database sinks
        SinkPipeline([MongoSink(db)]),
        # File system sinks
        SinkPipeline([JSONSink("./data/urls")]),
    ]
)


@with_retry(3)
def _fetch_max_pages_for_query(query: str):
    url = f"https://www.amazon.in/s?k={query}"

    res = make_get_request_with_proxy(url)
    if res is None:
        raise ValueError(f"Failed to fetch max pages for query: {query}")

    soup = bs4.BeautifulSoup(res.text, "html.parser")

    max_pages = soup.select(".s-pagination-item.s-pagination-disabled")
    if not max_pages:
        raise ValueError(f"Failed to fetch max pages for query: {query}")
    max_pages = max_pages[-1]
    if max_pages is None:
        raise ValueError(f"Failed to fetch max pages for query: {query}")
    max_pages = int(max_pages.get_text())

    return max_pages


@with_retry(3)
def _fetch_urls_on_page(query: str, page: int) -> list[str]:
    url = f"https://www.amazon.in/s?k={query}&page={page}&ref=nb_sb_noss_2"
    res = make_get_request_with_proxy(url)
    if res is None:
        raise ValueError(f"Failed to fetch URLs on page {page} for query: {query}")

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    links = soup.select(
        ".a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal"
    )

    urls: set[str] = set()
    for link in links:
        url = link.get("href")
        urls.add(f"https://www.amazon.in{url}")

    return list(urls)


@with_retry(3)
def _fetch_urls_for_query(query: str):
    logger.info(f"🔍 Fetching URLs for query: {query}")
    max_pages = 1
    try:
        max_pages = _fetch_max_pages_for_query(query)
    except:
        pass
    max_pages = 1
    logger.info(f"✅ Found {max_pages} pages".rjust(4))

    all_urls = []
    for page in range(1, max_pages + 1):
        urls = []
        try:
            urls = _fetch_urls_on_page(query, page)
        except:
            pass
        logger.info(f"✅ Found {len(urls)} URLs on page {page}".rjust(8))

        all_urls.extend(urls)

    logger.info(f"✅ Found {len(all_urls)} URLs".rjust(4))

    sink.dump_to_location(f"urls/{query}", {"query": query, "urls": all_urls})

    return all_urls


def _scrape_product_links_for_queries(queries: list[str]):
    with ThreadPoolExecutor(
        max_workers=THREAD_POOL_MAX_WORKERS,
        thread_name_prefix="amazon-scrapper_urls",
    ) as thread_pool:
        for query in queries:
            thread_pool.submit(_fetch_urls_for_query, query)
        thread_pool.shutdown(wait=True)


def scrape_product_links():
    queries = db["queries"].find()
    queries = map(lambda x: x["queries"], queries)
    queries = [item for sublist in queries for item in sublist]
    queries = sorted(list(set(queries)))

    # queries = queries[:1]

    _scrape_product_links_for_queries(queries)


def main():
    os.system("clear")

    scrape_product_links()
