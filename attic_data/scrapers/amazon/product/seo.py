import bs4
from attic_data.types.product import ProductSeo
from attic_data.types.scraper import BS4Scraper


class AmazonProductSEOScraper(BS4Scraper[ProductSeo]):
    def __init__(self, soup: bs4.BeautifulSoup):
        super().__init__(soup, [self._scrape_generic_seo])

    def _scrape_generic_seo(self) -> ProductSeo | None:
        title, description, keywords, canonical_url = "", "", "", ""

        # --- Title -----------------------------------------------------------

        title_element = self.find_element("title")
        if title_element:
            title = title_element.text

        # --- Description -----------------------------------------------------

        description_element = self.find_element('meta[name="description"]')
        if description_element:
            description = str(description_element["content"])

        # --- Keywords --------------------------------------------------------

        keywords_element = self.find_element('meta[name="keywords"]')
        if keywords_element:  # If found, use the keywords
            keywords = str(keywords_element["content"])
        else:  # If not found, check for alternative keywords in Open Graph
            og_keywords_element = self.find_element('meta[property="og:keywords"]')
            if og_keywords_element:
                keywords = str(og_keywords_element["content"])

        # --- Canonical URL --------------------------------------------------

        canonical_url_element = self.find_element('link[rel="canonical"]')
        if canonical_url_element:
            canonical_url = str(canonical_url_element["href"])

        # ---------------------------------------------------------------------

        if not title and not description and not keywords and not canonical_url:
            return None

        return ProductSeo(
            meta_title=title,
            meta_description=description,
            meta_keywords=keywords,
            canonical_url=canonical_url,
        )
