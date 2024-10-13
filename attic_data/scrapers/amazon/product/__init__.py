import random

import bs4
import requests

from attic_data.core.logging import logger
from attic_data.core.request import make_get_request_with_proxy
from attic_data.core.utils import logged_try_except, prepare_headers
from attic_data.scrapers.amazon.product.media import AmazonProductMediascraper
from attic_data.scrapers.amazon.product.price import AmazonProductPricescraper
from attic_data.scrapers.amazon.product.title import AmazonProductTitlescraper
from attic_data.types.product import *
from attic_data.types.sink import Sink


class AmazonProductscraper:
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

    def _articulate(self):
        if not self._soup:
            raise Exception("Soup not initialized")

        # Extracting product details
        title = title = AmazonProductTitlescraper(self._soup).scrape().value
        logger.info(f"    ✅ Title: {title}")
        price = AmazonProductPricescraper(self._soup).scrape().value
        logger.info(f"    ✅ Price: {price}")
        media = AmazonProductMediascraper(self._soup).scrape().value
        logger.info(f"    ✅ Media: {media}")

        product = Product.with_empty_values(self.url.split("/")[3])
        product.url = self._url

        # --- Media
        if media:
            product.media = media

        # --- Listing
        product.listing.sku = generate_id()
        product.listing.title = title or ""
        product.listing.seo.meta_title = title or ""

        # --- Details
        # --- Variants
        # --- Reviews

        self._product = product

    def _init_soup(self):
        if self._soup:
            return

        res = make_get_request_with_proxy(self._url)
        if not res:
            raise Exception("Failed to fetch product page")
        self._soup = bs4.BeautifulSoup(res.text, "html.parser")

    def scrape(self):
        logger.info(f"📡 Fetching product ({self._url})")

        self._has_failed = True
        with logged_try_except("amazon_product_scraper"):
            self._init_soup()
            self._articulate()
        self._has_failed = False

    def dump(self, sink: Sink):
        if not self._product:
            raise Exception("Product not scraped yet")

        logger.info(f"📦 Dumping product to sink ({self._product.id})")

        path = f"products/{self._product.id}"
        sink.dump_to_location_safe(path, self._product.model_dump())
