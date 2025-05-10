# tasks.py
from celery import shared_task
from scrapers.factory import ScraperFactory


@shared_task
def refresh_prices(site: str = "flipkart", keyword: str = "smartphones"):
    scraper = ScraperFactory.get_scraper(site)
    scraper.scrape(keyword)
