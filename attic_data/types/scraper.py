from typing import Callable, TypeVar, Any, override

import bs4

T = TypeVar("T")
ScraperFn = Callable[[], T | None]
ScraperFnList = list[ScraperFn[T]]


class Scraper[T]:
    _value: T | None
    _scrapers: ScraperFnList[T]

    @property
    def value(self):
        return self._value

    def __init__(self, scrapers: ScraperFnList[T]):
        self._value = None
        self._scrapers = scrapers

    def scrape(self):
        for scraper in self._scrapers:
            value = scraper()
            if value:
                self._value = value
                break

    def find_element(self, selector: str) -> Any:
        raise NotImplementedError(
            f"find_element method called for selector {selector} not implemented for {self.__class__.__name__}"
        )


class BS4Scraper[T](Scraper[T]):
    soup: bs4.BeautifulSoup

    def __init__(self, soup: bs4.BeautifulSoup, scrapers: ScraperFnList[T]):
        super().__init__(scrapers)
        self.soup = soup

    @override
    def find_element(self, selector: str) -> bs4.element.Tag | None:
        element = self.soup.select(selector)
        return element[0] if element else None
