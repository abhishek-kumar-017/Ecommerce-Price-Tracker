from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time


class FlipkartScraper:

    def __init__(self, keyword):
        self.keyword = keyword
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)

    def scrape(self):
        products = []
        for page in range(1, 3):  # You can scrape more pages if needed
            url = f"https://www.flipkart.com/search?q={self.keyword}&page={page}"
            self.driver.get(url)
            time.sleep(2)  # Wait for JS to render

            containers = self.driver.find_elements(By.CLASS_NAME, '_1AtVbE')

            for item in containers:
                try:
                    title = item.find_element(By.CLASS_NAME, '_4rR01T').text
                    price = item.find_element(By.CLASS_NAME,
                                              '_30jeq3').text.replace(
                                                  '₹', '').replace(',', '')
                    rating = item.find_element(By.CLASS_NAME, '_3LWZlK').text

                    # Extract review count (optional)
                    reviews_elem = item.find_elements(By.CLASS_NAME, '_2_R_DZ')
                    if reviews_elem:
                        text = reviews_elem[0].text
                        import re
                        match = re.search(r'(\d+(?:,\d+)*)\s+Reviews', text)
                        reviews = int(match.group(1).replace(
                            ',', '')) if match else None
                    else:
                        reviews = None

                    products.append({
                        'title': title,
                        'price': float(price),
                        'rating': float(rating),
                        'reviews': reviews,
                        'seller': "Flipkart"
                    })
                except Exception:
                    continue

        self.driver.quit()
        return products
