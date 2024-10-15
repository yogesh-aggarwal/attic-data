import random

import bs4
import requests

from attic_data.core.logging import logger
from attic_data.core.request import make_get_request_with_proxy
from attic_data.core.utils import logged_try_except, prepare_headers, with_retry
from attic_data.scrapers.amazon.product.description import (
    AmazonProductDescriptionScraper,
)
from attic_data.scrapers.amazon.product.media import AmazonProductMediascraper
from attic_data.scrapers.amazon.product.price import AmazonProductPricescraper
from attic_data.scrapers.amazon.product.seo import AmazonProductSEOScraper
from attic_data.scrapers.amazon.product.title import AmazonProductTitlescraper
from attic_data.types.product import *
from attic_data.types.sink import Sink


class AmazonProductscraper:
    _url: str
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
    def product(self):
        return self._product

    def dump(self, sink: Sink):
        if not self._product:
            raise Exception("Product not scraped yet")

        logger.info(f"📦 Dumping product to sink ({self._product.id})")

        path = f"products/{self._product.id}"
        sink.dump_to_location_safe(path, self._product.model_dump())

    def _init_soup(self):
        res = make_get_request_with_proxy(self._url)
        if not res:
            raise Exception("Failed to fetch product page")
        self._soup = bs4.BeautifulSoup(res.text, "html.parser")

    def _articulate(self):
        if not self._soup:
            raise Exception("Soup not initialized")

        # ---------------------------------------------------------------------
        # -- Extracting product details
        # ---------------------------------------------------------------------

        # --- Title
        title = title = AmazonProductTitlescraper(self._soup).scrape().value
        logger.info(f"    ✅ Title: {title}")

        # --- Description
        description = AmazonProductDescriptionScraper(self._soup).scrape().value
        logger.info(f"    ✅ Description: {description}")

        # --- Price
        price = AmazonProductPricescraper(self._soup).scrape().value
        logger.info(f"    ✅ Price: {price}")

        # --- Media
        media = AmazonProductMediascraper(self._soup).scrape().value
        logger.info(f"    ✅ Media: {media}")

        # --- SEO
        seo = AmazonProductSEOScraper(self._soup).scrape().value
        logger.info(f"    ✅ SEO: {seo}")

        # ---------------------------------------------------------------------

        assert (
            title and description and price and media and seo
        ), "Failed to scrape product details"

        # ---------------------------------------------------------------------

        product = Product.with_empty_values(self.url.split("/")[3])
        product.url = self._url

        # --- Media -----------------------------------------------------------

        if media:
            product.media = media

        # --- Listing ---------------------------------------------------------

        product.listing.sku = generate_id()
        product.listing.title = title
        product.listing.description = description
        product.listing.seo = seo

        product.listing

        # --- Details ---------------------------------------------------------
        # --- Variants --------------------------------------------------------
        # --- Reviews ---------------------------------------------------------

        self._product = product

    @with_retry(128)
    def scrape(self):
        logger.info(f"📡 Fetching product ({self._url})")

        self._init_soup()
        self._articulate()
