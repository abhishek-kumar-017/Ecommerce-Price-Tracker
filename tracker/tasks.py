# tasks.py
from celery import shared_task
from scrappers.factory import ScraperFactory


@shared_task
def refresh_prices(site: str = "flipkart", keyword: str = "smartphones"):
    scraper = ScraperFactory.get_scraper(site)
    scraper.scrape(keyword)
