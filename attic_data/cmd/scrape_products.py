import bs4
import requests

from attic_data.core.logging import logger
from attic_data.core.utils import cd, prepare_headers


def _scrape_product(url: str):
    res = requests.get(url, headers=prepare_headers())
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    logger.info(f"\t✅ Title: {'title'}")


def _scrape_products_from_urls(urls: list[str]):
    for url in urls:
        _scrape_product(url)


def scrape_products_from_urls_file(file_path: str):
    with cd("data"):
        with open(file_path, "r") as f:
            urls = [url.strip() for url in f.readlines()]
            urls = urls[-1:]

        _scrape_products_from_urls(urls)


def main():
    scrape_products_from_urls_file("urls.txt")
