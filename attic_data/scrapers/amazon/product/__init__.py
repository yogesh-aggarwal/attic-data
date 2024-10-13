import bs4
import requests

from attic_data.core.logging import logger
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

    def _articulate(self) -> Product:
        # Extracting product details
        title = title = AmazonProductTitlescraper(self.soup).scrape().value
        logger.info(f"\t✅ Title: {title}")
        price = AmazonProductPricescraper(self.soup).scrape().value
        logger.info(f"\t✅ Price: {price}")
        media = AmazonProductMediascraper(self.soup).scrape().value
        logger.info(f"\t✅ Media: {media}")

        product = Product.with_empty_values(self.url.split("/")[3])

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

        return product

    def scrape(self):
        self._has_failed = True
        with logged_try_except("🕸️ amazon_product_scraper"):
            res = requests.get(self._url, headers=prepare_headers())
            res.raise_for_status()

            self.soup = bs4.BeautifulSoup(res.text, "html.parser")

            self._product = self._articulate()
        self._has_failed = False

    def dump(self, sink: Sink):
        if not self._product:
            raise Exception("Product not scraped yet")

        path = f"products/{self._product.id}"
        sink.dump_to_location(path, self._product.model_dump())
