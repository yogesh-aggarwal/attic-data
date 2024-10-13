import bs4

from attic_data.types.scraper import BS4Scraper


class AmazonProductTitleScrapper(BS4Scraper[str]):
    def __init__(self, soup: bs4.BeautifulSoup):
        super().__init__(soup, [self._scrape_generic_title])

    def _scrape_generic_title(self) -> str | None:
        value: str | None = None

        element = self.soup.select("#productTitle")
        if element:
            value = element[0].text.strip()

        return value
