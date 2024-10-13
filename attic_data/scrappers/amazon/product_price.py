import re
import bs4

from attic_data.core.logging import logger


class AmazonProductPriceScrapper:
    soup: bs4.BeautifulSoup
    _value: float | None

    @property
    def value(self):
        return self._value

    def __init__(self, soup: bs4.BeautifulSoup):
        self.soup = soup
        self._value = None

    def _util_extract_price_from_text(self, text: str) -> float | None:
        value: float | None = None

        element = re.findall(r"\d+", text)
        if element:
            value = float("".join(element[:-1]) + "." + element[-1].lstrip("0"))

        return value

    def _scrape_generic_price(self) -> float | None:
        value: float | None = None

        element = self.soup.select(".a-price")
        if element:
            value = self._util_extract_price_from_text(element[0].text)

        return value

    def _scrape_kindle_price(self) -> float | None:
        value: float | None = None

        element = self.soup.select("#kindle-price")
        if element:
            value = self._util_extract_price_from_text(element[0].text)

        return value

    def scrape(self):
        scrapers = [self._scrape_generic_price, self._scrape_kindle_price]
        for scraper in scrapers:
            value = scraper()
            if value is not None:
                self._value = value
                break
