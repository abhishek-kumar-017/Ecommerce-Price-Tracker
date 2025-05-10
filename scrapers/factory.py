# scrapers/factory.py
from scrapers.flipkart_scraper import FlipkartScraper
from scrapers.amazon_scraper import AmazonScraper


class ScraperFactory:
    scrapers = {'flipkart': FlipkartScraper, 'amazon': AmazonScraper}

    @staticmethod
    def get_scraper(site_name: str):
        scraper_class = ScraperFactory.scrapers.get(site_name.lower())
        if not scraper_class:
            raise ValueError(f"No scraper found for site: {site_name}")
        return scraper_class()
