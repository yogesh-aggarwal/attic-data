import os
from concurrent.futures import ThreadPoolExecutor

from pymongo import MongoClient

from attic_data.core.constants import MONGO_URI, THREAD_POOL_MAX_WORKERS
from attic_data.core.logging import logger
from attic_data.scrapers.amazon.product import AmazonProductscraper
from attic_data.types.sink.json import JSONSink
from attic_data.types.sink.mongo import MongoSink
from attic_data.types.sink.pipeline import SinkPipeline

db = MongoClient(MONGO_URI)["attic"]
sink = SinkPipeline(
    [
        # Database sinks
        SinkPipeline([MongoSink(db)]),
        # File system sinks
        SinkPipeline([JSONSink("./data/products")]),
    ]
)


def _scrape_product_from_url(url: str):
    scraper = AmazonProductscraper(url)
    scraper.scrape()
    if scraper.has_failed:
        logger.error(f"❌ Failed to scrape product: {url}")
    else:
        scraper.dump(sink)
        logger.info(f"🆗 Product scraped: {url}")


def scrape_products():
    failed_urls = []

    def _scrape(url: str):
        try:
            _scrape_product_from_url(url)
        except Exception as e:
            logger.error(f"❌ Failed to scrape product: {e}")

            failed_urls.append(url)
            with open("failed_urls.txt", "w+") as f:
                for url in failed_urls:
                    f.write(f"{url}\n")

    queries_urls = db["urls"].find()

    with ThreadPoolExecutor(
        max_workers=THREAD_POOL_MAX_WORKERS,
        thread_name_prefix="amazon-scrapper_product",
    ) as thread_pool:
        for query_url in queries_urls:
            urls = query_url["urls"]
            for url in urls:
                thread_pool.submit(_scrape, url)
        thread_pool.shutdown(wait=True)


def main():
    os.system("clear")

    scrape_products()
