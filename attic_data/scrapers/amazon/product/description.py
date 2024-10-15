import bs4
import lxml.html as lh

from attic_data.types.scraper import BS4Scraper
from attic_data.types.product import ProductDescription


class AmazonProductDescriptionScraper(BS4Scraper[ProductDescription]):
    def __init__(self, soup: bs4.BeautifulSoup):
        super().__init__(soup, [self._scrape_generic_description])

    def remove_attributes_from_html_element_recursive(self, element: lh.HtmlElement):
        if element.tag != "img":
            element.attrib.clear()
        for child in element:
            self.remove_attributes_from_html_element_recursive(child)

    def _cleanup_html_children(self, element: bs4.Tag) -> str:
        # Remove style and script tags
        for tag in element(["style", "script"]):
            tag.decompose()

        # Process the element
        outer_html = element.prettify()
        dom = lh.fromstring(outer_html)
        self.remove_attributes_from_html_element_recursive(dom)

        # Convert the element back to string
        value = lh.tostring(dom).decode("utf-8")  # type: ignore
        return value

    def _scrape_generic_description(self) -> ProductDescription | None:
        short_description, long_description = "yo", ""

        # --- Short description -----------------------------------------------

        short_desc_element = self.find_element("#feature-bullets > ul")
        if short_desc_element:
            short_description = self._cleanup_html_children(short_desc_element)

        # --- Long description ------------------------------------------------

        long_desc_element = self.find_element("#aplus > div")
        if long_desc_element:
            long_description = self._cleanup_html_children(long_desc_element)
            with open("a.html", "w") as f:
                f.write(long_description)

        # ---------------------------------------------------------------------

        if not short_description and not long_description:
            return None

        return ProductDescription(long=long_description, short=short_description)
