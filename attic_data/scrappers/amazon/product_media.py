import re
import bs4

from attic_data.core.logging import logger
from attic_data.types.product import ProductMedia, ProductMediaImage, ProductMediaVideo


class AmazonProductMediaScrapper:
    soup: bs4.BeautifulSoup
    _value: ProductMedia | None

    @property
    def value(self):
        return self._value

    def __init__(self, soup: bs4.BeautifulSoup):
        self.soup = soup
        self._value = None

    def _scrape_generic_media(self) -> ProductMedia | None:
        media = ProductMedia(images=[], videos=[])

        return None

    def _scrape_kindle_media(self) -> ProductMedia | None:
        media = ProductMedia(images=[], videos=[])

        element = self.soup.select_one("#landingImage")
        if element:
            url: str = element.get("src", None)  # type: ignore
            alt_text: str = element.get("alt", None)  # type: ignore
            if url and alt_text:
                media.images.append(ProductMediaImage(url=url, alt_text=alt_text))
        return media

    def scrape(self):
        scrapers = [self._scrape_generic_media, self._scrape_kindle_media]
        for scraper in scrapers:
            value = scraper()
            if value is not None:
                self._value = value
                break
