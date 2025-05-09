# scrapers/flipkart_scraper.py
import requests
from bs4 import BeautifulSoup
from .base import BaseScraper
from tracker.models import Product, PriceHistory


class FlipkartScraper(BaseScraper):

    def scrape(self, keyword):
        headers = {"User-Agent": "Mozilla/5.0"}
        for page in range(1, 3):
            url = f"https://www.flipkart.com/search?q={keyword}&page={page}"
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            for item in soup.select("._1AtVbE"):
                title_tag = item.select_one("._4rR01T")
                price_tag = item.select_one("._30jeq3")
                if not title_tag or not price_tag:
                    continue

                title = title_tag.get_text()
                price = float(price_tag.text.strip("₹").replace(",", ""))
                product, _ = Product.objects.update_or_create(
                    title=title,
                    defaults={
                        "current_price": price,
                        "url": url
                    },
                )
                PriceHistory.objects.create(product=product, price=price)
