# tasks.py
from celery import shared_task
from scrapers.factory import ScraperFactory
from celery import shared_task
from .models import Product, PriceHistory
from scrapers.flipkart_scraper import FlipkartScraper
from decimal import Decimal


@shared_task
def refresh_prices(site: str = "flipkart", keyword: str = "smartphones"):
    scraper = ScraperFactory.get_scraper(site)
    scraper.scrape(keyword)


@shared_task
def scrape_and_save_flipkart_products(query="smartphone", max_pages=1):
    products = FlipkartScraper.scrape_flipkart_products(query, max_pages)

    for item in products:
        obj, created = Product.objects.get_or_create(
            title=item['title'],
            defaults={
                'price':
                Decimal(item['price']),
                'rating':
                float(item['rating']) if item.get('rating') else None,
                'num_reviews':
                int(item['num_reviews'].replace(',', ''))
                if item.get('num_reviews') else None,
                'seller_name':
                'Flipkart'  # placeholder
            })
        # Add new price entry even if product exists
        PriceHistory.objects.create(product=obj, price=Decimal(item['price']))

    return f"Scraped {len(products)} products for '{query}'"
