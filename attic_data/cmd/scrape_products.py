import os
import bs4
import requests
import re

from attic_data.core.logging import logger
from attic_data.core.utils import cd, prepare_headers
from attic_data.scrappers.product import ProductScrapper


def _scrape_products_from_urls(urls: list[str]):
    failed_urls = []
    for url in urls:
        scrapper = ProductScrapper(url)
        scrapper.scrape()
        if scrapper.has_failed:
            failed_urls.append(url)

    if failed_urls:
        with open("failed_urls.txt", "w") as f:
            for url in failed_urls:
                f.write(f"{url}\n")


def scrape_products_from_urls_file(file_path: str):
    with cd("data"):
        with open(file_path, "r") as f:
            urls = [url.strip() for url in f.readlines()]
            urls = urls[0:1]

        _scrape_products_from_urls(urls)


def main():
    os.system("clear")
    scrape_products_from_urls_file("urls.txt")
