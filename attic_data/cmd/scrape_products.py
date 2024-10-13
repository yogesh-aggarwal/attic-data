import os

from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

from attic_data.core.constants import MONGO_URI
from attic_data.core.logging import logger
from attic_data.core.utils import cd
from attic_data.scrapers.amazon.product import AmazonProductscraper
from attic_data.types.sink.file import FileSink
from attic_data.types.sink.json import JSONSink
from attic_data.types.sink.mongo import MongoSink
from attic_data.types.sink.pipeline import SinkPipeline

os.system("clear")

db = MongoClient(MONGO_URI)["attic"]
sink = SinkPipeline(
    [
        # Database sinks
        SinkPipeline(
            [
                MongoSink(db),
            ]
        ),
        # File system sinks
        SinkPipeline(
            [
                JSONSink("./data"),
                # FileSink(),
            ]
        ),
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


def _scrape_products_from_urls(urls: list[str]):
    failed_urls = []

    with ThreadPoolExecutor(
        max_workers=16,
        thread_name_prefix="amazon-scrapper_product",
    ) as pool:
        for url in urls:
            pool.submit(_scrape_product_from_url, url)

    if failed_urls:
        with open("failed_urls.txt", "w+") as f:
            for url in failed_urls:
                f.write(f"{url}\n")


def scrape_products_from_urls_file(file_path: str):
    with cd("data"):
        with open(file_path, "r") as f:
            urls = [url.strip() for url in f.readlines()]
            urls = urls

        _scrape_products_from_urls(urls)


def main():
    scrape_products_from_urls_file("urls.txt")
