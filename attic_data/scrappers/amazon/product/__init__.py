import bs4
import requests

from attic_data.core.logging import logger
from attic_data.core.utils import prepare_headers, logged_try_except
from attic_data.scrappers.amazon.product.media import AmazonProductMediaScrapper
from attic_data.scrappers.amazon.product.price import AmazonProductPriceScrapper
from attic_data.scrappers.amazon.product.title import AmazonProductTitleScrapper
from attic_data.types.product import *


class AmazonProductScrapper:
    _url: str
    _has_failed: bool
    _soup: bs4.BeautifulSoup | None
    _product: Product | None

    def __init__(self, url: str):
        self._url = url
        self._has_failed = False
        self._soup = None
        self._product = None

    @property
    def url(self):
        return self._url

    @property
    def has_failed(self):
        return self._has_failed

    @property
    def product(self):
        return self._product

    def _articulate(self) -> Product:
        # Extracting product details
        title = title = AmazonProductTitleScrapper(self.soup).scrape().value
        logger.info(f"\t✅ Title: {title}")
        price = AmazonProductPriceScrapper(self.soup).scrape().value
        logger.info(f"\t✅ Price: {price}")
        media = AmazonProductMediaScrapper(self.soup).scrape().value
        logger.info(f"\t✅ Media: {media}")

        product = Product.with_empty_values()

        # --- Media
        if media:
            product.media = media

        # --- Listing
        product.listing.title = title or ""
        product.listing.seo.meta_title = title or ""

        # --- Details
        # --- Variants
        # --- Reviews

        return product

    def scrape(self):
        self._has_failed = True
        with logged_try_except("🕸️ amazon_product_scrapper"):
            res = requests.get(self._url, headers=prepare_headers())
            res.raise_for_status()

            self.soup = bs4.BeautifulSoup(res.text, "html.parser")

            self._product = self._articulate()
        self._has_failed = False
