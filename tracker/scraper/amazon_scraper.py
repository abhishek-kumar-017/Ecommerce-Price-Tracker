import requests
from bs4 import BeautifulSoup
import re


class AmazonScraper:

    def __init__(self, keyword):
        self.keyword = keyword
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
            ' Chrome/58.0.3029.110 Safari/537.3'
        }

    def scrape(self):
        products = []
        for page in range(1, 3):  # Scrape first 2 pages
            url = f'https://www.amazon.in/s?k={self.keyword}&page={page}'
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            results = soup.find_all('div',
                                    {'data-component-type': 's-search-result'})

            for item in results:
                title_elem = item.h2
                title = title_elem.text.strip() if title_elem else None

                price_whole = item.find('span', 'a-price-whole')
                price_fraction = item.find('span', 'a-price-fraction')
                if price_whole and price_fraction:
                    price = float(
                        price_whole.text.replace(',', '') + '.' +
                        price_fraction.text)
                else:
                    price = None

                rating_elem = item.find('span', {'class': 'a-icon-alt'})
                rating = float(
                    rating_elem.text.split()[0]) if rating_elem else None

                review_elem = item.find('span', {'class': 'a-size-base'})
                reviews = int(review_elem.text.replace(
                    ',', '')) if review_elem and review_elem.text.replace(
                        ',', '').isdigit() else None

                seller = "Amazon"  # Seller info is not readily available on the search page

                if title and price:
                    products.append({
                        'title': title,
                        'price': price,
                        'rating': rating,
                        'reviews': reviews,
                        'seller': seller
                    })
        return products
