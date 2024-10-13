import re
import bs4

from attic_data.core.logging import logger


class ProductTitleScrapper:
    soup: bs4.BeautifulSoup
    _value: str | None

    @property
    def title(self):
        return self._value

    def __init__(self, soup: bs4.BeautifulSoup):
        self.soup = soup
        self._value = None

    def _scrape_generic_title(self) -> str | None:
        value: str | None = None

        element = self.soup.select("#productTitle")
        if element:
            value = element[0].text.strip()

        return value

    def scrape(self):
        scrapers = [self._scrape_generic_title]
        for scraper in scrapers:
            title = scraper()
            if title:
                self._value = title
                break
