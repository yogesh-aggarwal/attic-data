import requests
import bs4

from attic_data.core.logging import logger
from attic_data.core.utils import prepare_headers
from attic_data.scrappers.product_price import ProductPriceScrapper
from attic_data.scrappers.product_title import ProductTitleScrapper


class ProductScrapper:
    _url: str
    _has_failed: bool

    def __init__(self, url: str):
        self._url = url
        self._has_failed = False

    @property
    def url(self):
        return self._url

    @property
    def has_failed(self):
        return self._has_failed

    def _scrape_title(self, soup) -> str | None:
        title_scrapper = ProductTitleScrapper(soup)
        title_scrapper.scrape()

        logger.info(f"\t✅ Title: {title_scrapper.title}")
        return title_scrapper.title

    def _scrape_price(self, soup) -> float | None:
        price_scrapper = ProductPriceScrapper(soup)
        price_scrapper.scrape()

        logger.info(f"\t✅ Price: {price_scrapper.price}")
        return price_scrapper.price

    def scrape(self):
        res = requests.get(self._url, headers=prepare_headers())
        soup = bs4.BeautifulSoup(res.text, "html.parser")

        try:
            title = self._scrape_title(soup)
            price = self._scrape_price(soup)
        except Exception as e:
            logger.error(f"\t❌ Error: {e}")
            self._has_failed = True
