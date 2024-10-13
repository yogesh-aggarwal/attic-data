import bs4

from attic_data.types.product import ProductMedia, ProductMediaImage, ProductMediaVideo
from attic_data.types.scraper import BS4Scraper


class AmazonProductMediaScrapper(BS4Scraper[ProductMedia]):
    def __init__(self, soup: bs4.BeautifulSoup):
        super().__init__(soup, [self._scrape_generic_media, self._scrape_kindle_media])

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
