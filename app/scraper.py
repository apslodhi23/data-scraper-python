from bs4 import BeautifulSoup
import requests
import time
import redis
from pydantic import ValidationError

from app.notification.notification_strategy import NotificationStrategy
from app.settings import IMAGE_FOLDER, REDIS_DB, REDIS_HOST, REDIS_PORT
from app.storage.storage_strategy import StorageStrategy
from .models import Settings, Product
from .utils import download_image

class Scraper:
    def __init__(self, settings: Settings, storage_strategy: StorageStrategy, notification_strategy: NotificationStrategy):
        self.settings = settings
        self.storage_strategy = storage_strategy
        self.notification_strategy = notification_strategy
        self.base_url = "https://dentalstall.com/shop/"
        self.products = []
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    def scrape(self):
        page = 1
        total_skipped = 0
        while True:
            if self.settings.limit and page > self.settings.limit:
                break

            url = f"{self.base_url}?page={page}"
            print(f"Scraping URL: {url}")
            response = self.get_response(url)
            if not response:
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            product_elements = soup.select("li.product")
            if not product_elements:
                print(f"No product elements found on page {page}.")
                break

            page_skipped = 0
            for product in product_elements:
                product_title_elem = product.select_one(".woo-loop-product__title a")
                product_price_elem = product.select_one(".price .woocommerce-Price-amount bdi")
                image_elem = product.select_one(".mf-product-thumbnail img")

                if not product_title_elem or not product_price_elem or not image_elem:
                    print(f"Skipping a product on page {page} due to missing elements. Title: {bool(product_title_elem)}, Price: {bool(product_price_elem)}, Image: {bool(image_elem)}")
                    page_skipped += 1
                    continue

                product_title = product_title_elem.text.strip()
                try:
                    product_price = float(product_price_elem.text.strip().replace('₹', '').replace(',', ''))
                except ValueError:
                    print(f"Skipping a product on page {page} due to invalid price format. Title: {product_title}")
                    page_skipped += 1
                    continue

                image_url = image_elem.get("data-lazy-src") or image_elem.get("src")
                if not image_url:
                    print(f"Skipping a product on page {page} due to missing image URL. Title: {product_title}")
                    page_skipped += 1
                    continue

                image_path = download_image(image_url, IMAGE_FOLDER)

                try:
                    product = Product(product_title=product_title, product_price=product_price, path_to_image=image_path)
                    self.products.append(product)
                except ValidationError as e:
                    print(f"Skipping a product on page {page} due to validation error: {e}")
                    page_skipped += 1

            total_skipped += page_skipped
            print(f"Page {page} summary: Total products: {len(product_elements)}, Skipped: {page_skipped}")
            page += 1

        final_message = f"Scraping completed. Total products scraped: {len(self.products)}, Total skipped: {total_skipped}"
        self.notification_strategy.send_notification(final_message)

    def get_response(self, url: str):
        retries = 3
        for attempt in range(retries):
            try:
                proxies = {"http": self.settings.proxy, "https": self.settings.proxy} if self.settings.proxy else None
                response = requests.get(url, proxies=proxies)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                print(f"Request failed (attempt {attempt + 1}/{retries}): {e}. Retrying in 5 seconds...")
                time.sleep(5)
        print(f"Failed to retrieve URL after {retries} attempts: {url}")
        return None

    def cache_and_store_results(self) -> int:
        current_data = self.storage_strategy.load()
        current_titles = {product["product_title"]: product for product in current_data}

        updated_count = 0
        for product in self.products:
            cached_price = self.redis_client.get(product.product_title)
            if cached_price and float(cached_price) == product.product_price:
                continue

            self.redis_client.set(product.product_title, product.product_price)
            if product.product_title in current_titles:
                if current_titles[product.product_title]["product_price"] != product.product_price:
                    current_titles[product.product_title] = product.dict()
                    updated_count += 1
            else:
                current_titles[product.product_title] = product.dict()
                updated_count += 1

        self.storage_strategy.save(list(current_titles.values()))
        return updated_count
