import requests
import bs4

from attic_data.core.logging import logger
from attic_data.core.utils import prepare_headers
from attic_data.types.product import ProductMedia
from attic_data.scrappers.amazon.product_media import AmazonProductMediaScrapper
from attic_data.scrappers.amazon.product_price import AmazonProductPriceScrapper
from attic_data.scrappers.amazon.product_title import AmazonProductTitleScrapper


class AmazonProductScrapper:
    _url: str
    _has_failed: bool
    _soup: bs4.BeautifulSoup

    def __init__(self, url: str):
        self._url = url
        self._has_failed = False

    @property
    def url(self):
        return self._url

    @property
    def has_failed(self):
        return self._has_failed

    def _scrape_title(self) -> str | None:
        scrapper = AmazonProductTitleScrapper(self._soup)
        scrapper.scrape()

        logger.info(f"\t✅ Title: {scrapper.value}")
        return scrapper.value

    def _scrape_price(self) -> float | None:
        scrapper = AmazonProductPriceScrapper(self._soup)
        scrapper.scrape()

        logger.info(f"\t✅ Price: {scrapper.value}")
        return scrapper.value

    def _scrape_media(self) -> ProductMedia | None:
        scrapper = AmazonProductMediaScrapper(self._soup)
        scrapper.scrape()

        logger.info(f"\t✅ Media: {scrapper.value}")
        return scrapper.value

    def scrape(self):
        res = requests.get(self._url, headers=prepare_headers())
        self._soup = bs4.BeautifulSoup(res.text, "html.parser")

        try:
            title = self._scrape_title()
            price = self._scrape_price()
            media = self._scrape_media()
        except Exception as e:
            logger.error(f"\t❌ Error: {e}")
            self._has_failed = True
