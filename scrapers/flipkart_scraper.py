import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager

from scrapers.base import BaseScraper


class FlipkartScraper(BaseScraper):

    # def scrape(self, keyword):
    #     headers = {"User-Agent": "Mozilla/5.0"}
    #     for page in range(1, 3):
    #         url = f"https://www.amazon.com/search?q={keyword}&page={page}"
    #         response = requests.get(url, headers=headers)
    #         soup = BeautifulSoup(response.text, "html.parser")

    #         for item in soup.select("._1AtVbE"):
    #             title_tag = item.select_one("._4rR01T")
    #             price_tag = item.select_one("._30jeq3")
    #             if not title_tag or not price_tag:
    #                 continue

    #             title = title_tag.get_text()
    #             price = float(price_tag.text.strip("₹").replace(",", ""))
    #             product, _ = Product.objects.update_or_create(
    #                 title=title,
    #                 defaults={
    #                     "current_price": price,
    #                     "url": url
    #                 },
    #             )
    #             PriceHistory.objects.create(product=product, price=price)

    def scrape_flipkart_products(query, max_pages=1):
        # Firefox headless options
        options = Options()
        options.headless = True
        options.set_preference(
            "general.useragent.override",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:113.0) Gecko/20100101 Firefox/113.0"
        )

        driver = webdriver.Firefox(service=Service(
            GeckoDriverManager().install()),
                                   options=options)

        products = []

        for page in range(1, max_pages + 1):
            search_url = f"https://www.flipkart.com/search?q={query}&page={page}"
            driver.get(search_url)

            # Close login popup if it appears
            try:
                close_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(text(),'✕')]")))
                close_btn.click()
                time.sleep(1)
            except:
                pass

            try:
                # Wait for actual product containers
                product_cards = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//div[@data-id]")))
            except Exception as e:
                print(f"Page {page} failed to load products: {e}")
                continue

            for card in product_cards:
                try:
                    # Title
                    try:
                        title = card.find_element(By.CLASS_NAME,
                                                  '_4rR01T').text
                    except:
                        title = card.find_element(By.CLASS_NAME, 's1Q9rs').text

                    # Price
                    price = card.find_element(By.CLASS_NAME,
                                              '_30jeq3').text.replace(
                                                  '₹', '').replace(',', '')

                    # Rating (optional)
                    try:
                        rating = card.find_element(By.CLASS_NAME,
                                                   '_3LWZlK').text
                    except:
                        rating = None

                    # Reviews (optional)
                    try:
                        reviews = card.find_element(
                            By.CSS_SELECTOR, 'span._2_R_DZ span span').text
                    except:
                        reviews = None

                    products.append({
                        'title': title,
                        'price': price,
                        'rating': rating,
                        'num_reviews': reviews
                    })

                except Exception:
                    continue  # Skip broken entries

        driver.quit()
        return products
