from .amazon_scraper import AmazonScraper
from .flipkart_scraper import FlipkartScraper


class ScraperFactory:

    @staticmethod
    def get_scraper(site, keyword):
        if site == 'amazon':
            return AmazonScraper(keyword)
        elif site == 'flipkart':
            return FlipkartScraper(keyword)
        else:
            raise ValueError("Unsupported site")
