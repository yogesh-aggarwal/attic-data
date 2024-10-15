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
        SinkPipeline([JSONSink("./data")]),
    ]
)


def _scrape_product_from_url(url: str):
    scraper = AmazonProductscraper(url)
    try:
        scraper.scrape()
        scraper.dump(sink)
        logger.info(f"🆗 Product scraped: {url}")
    except:
        db["metadata"].update_one(
            {"_id": "tracking"},
            {"$push": {"products.failed_urls": url}},
        )
        logger.error(f"❌ Failed to scrape product: {url}")


def scrape_products():
    with ThreadPoolExecutor(
        max_workers=THREAD_POOL_MAX_WORKERS,
        thread_name_prefix="amazon-scrapper_product",
    ) as thread_pool:
        docs = db["urls"].find()
        for doc in docs:
            urls = doc["urls"]
            for url in urls:
                thread_pool.submit(_scrape_product_from_url, url)
        thread_pool.shutdown(wait=True)


def main():
    os.system("clear")

    scrape_products()
