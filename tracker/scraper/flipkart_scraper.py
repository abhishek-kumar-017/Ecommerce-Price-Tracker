import requests
from bs4 import BeautifulSoup
import re


class FlipkartScraper:

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
            url = f'https://www.flipkart.com/search?q={self.keyword}&page={page}'
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            results = soup.find_all('div', {'class': '_1AtVbE'})

            for item in results:
                title_elem = item.find('div', {'class': '_4rR01T'})
                title = title_elem.text.strip() if title_elem else None

                price_elem = item.find('div', {'class': '_30jeq3 _1_WHN1'})
                if price_elem:
                    price_text = price_elem.text.strip().replace('₹',
                                                                 '').replace(
                                                                     ',', '')
                    price = float(price_text) if price_text.isdigit() else None
                else:
                    price = None

                rating_elem = item.find('div', {'class': '_3LWZlK'})
                rating = float(
                    rating_elem.text.strip()) if rating_elem else None

                review_elem = item.find('span', {'class': '_2_R_DZ'})
                if review_elem:
                    review_text = review_elem.text.strip()
                    match = re.search(r'(\d+)', review_text.replace(',', ''))
                    reviews = int(match.group(1)) if match else None
                else:
                    reviews = None

                seller = "Flipkart"  # Seller info is not readily available on the search page

                if title and price:
                    products.append({
                        'title': title,
                        'price': price,
                        'rating': rating,
                        'reviews': reviews,
                        'seller': seller
                    })
        return products
