from django.core.management.base import BaseCommand
from tracker.scraper.factory import ScraperFactory
from tracker.models import Product, PriceHistory


class Command(BaseCommand):
    help = 'Scrape product data from a given site'

    def add_arguments(self, parser):
        parser.add_argument('--site', type=str, required=True)
        parser.add_argument('--keyword', type=str, required=True)

    def handle(self, *args, **options):
        scraper = ScraperFactory.get_scraper(options['site'],
                                             options['keyword'])
        print(
            f"Running scraper for {options['site']} with keyword '{options['keyword']}'"
        )

        data = scraper.scrape()
        for item in data:
            product, created = Product.objects.get_or_create(
                title=item['title'],
                defaults={
                    'price': item['price'],
                    'rating': item.get('rating'),
                    'reviews': item.get('reviews'),
                    'seller': item.get('seller'),
                    'source': options['site'],
                })
            print(f"Fetched {len(product)} products from {options['site']}")

            PriceHistory.objects.create(product=product, price=item['price'])
