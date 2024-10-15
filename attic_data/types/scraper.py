from typing import Callable, TypeVar, Any, override

import bs4

T = TypeVar("T")
ScraperFn = Callable[[], T | None]
ScraperFnList = list[ScraperFn[T]]


class Scraper[T]:
    _value: T | None
    _has_failed: bool
    _scrapers: ScraperFnList[T]

    @property
    def value(self):
        return self._value

    @property
    def has_failed(self):
        return self._has_failed

    def __init__(self, scrapers: ScraperFnList[T]):
        self._value = None
        self._has_failed = False
        self._scrapers = scrapers

    def scrape(self):
        for scraper in self._scrapers:
            value = scraper()
            if value:
                self._value = value
                break
        self._has_failed = self._value is None

        return self

    def find_element(self, selector: str) -> Any:
        raise NotImplementedError(
            f"find_element method called for selector {selector} not implemented for {self.__class__.__name__}"
        )

    def find_elements(self, selector: str) -> list[Any]:
        raise NotImplementedError(
            f"find_elements method called for selector {selector} not implemented for {self.__class__.__name__}"
        )

    def find_element_by_id(self, id_: str) -> Any:
        raise NotImplementedError(
            f"find_element_by_id method called for id {id_} not implemented for {self.__class__.__name__}"
        )

    def find_element_by_class(self, class_: str) -> Any:
        raise NotImplementedError(
            f"find_element_by_class method called for class {class_} not implemented for {self.__class__.__name__}"
        )

    def find_elements_by_class(self, class_: str) -> list[Any]:
        raise NotImplementedError(
            f"find_elements_by_class method called for class {class_} not implemented for {self.__class__.__name__}"
        )

    def find_element_by_tag(self, tag: str) -> Any:
        raise NotImplementedError(
            f"find_element_by_tag method called for tag {tag} not implemented for {self.__class__.__name__}"
        )

    def find_elements_by_tag(self, tag: str) -> list[Any]:
        raise NotImplementedError(
            f"find_elements_by_tag method called for tag {tag} not implemented for {self.__class__.__name__}"
        )


class BS4Scraper[T](Scraper[T]):
    _soup: bs4.BeautifulSoup

    def __init__(self, soup: bs4.BeautifulSoup, scrapers: ScraperFnList[T]):
        super().__init__(scrapers)
        self._soup = soup

    @override
    def find_element(self, selector: str) -> bs4.element.Tag | None:
        element = self._soup.select(selector)
        return element[0] if element else None

    @override
    def find_elements(self, selector: str) -> list[bs4.element.Tag]:
        return self._soup.select(selector)

    @override
    def find_element_by_id(self, id_: str) -> bs4.element.Tag | None:
        return self.find_element(f"#{id_}")

    @override
    def find_element_by_class(self, class_: str) -> bs4.element.Tag | None:
        class_ = class_.replace(" ", ".").replace(",", ".").replace("..", ".").strip()
        return self.find_element(class_)

    @override
    def find_elements_by_class(self, class_: str) -> list[bs4.element.Tag]:
        class_ = class_.replace(" ", ".").replace(",", ".").replace("..", ".").strip()
        return self.find_elements(class_)

    @override
    def find_element_by_tag(self, tag: str) -> bs4.element.Tag | None:
        return self.find_element(tag)

    @override
    def find_elements_by_tag(self, tag: str) -> list[bs4.element.Tag]:
        return self.find_elements(tag)
