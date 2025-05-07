import scrapy
from MicroModern.items import MicromodernItem
from datetime import datetime
import pandas as pd
import os
import pytz

class SisoogSpider(scrapy.Spider):
    name = "sisoog"
    allowed_domains = ["shop.sisoog.com"]
    user_input = input('part name: ')
    if user_input == 'all':
        start_urls = ["https://shop.sisoog.com/products/"]
    else:
        start_urls = [f"https://shop.sisoog.com/?s={user_input}&post_type=product&ct_product_price=1"]

    def __init__(self, *args, **kwargs):
        super(SisoogSpider, self).__init__(*args, **kwargs)
        self.items = []  # Initialize a list to hold scraped items

    def parse(self, response):
        product_cards = response.xpath("//li[contains(@class, 'product')]")
        for card in product_cards:
            # Extract product name
            part_name = card.xpath(".//h2[contains(@class, 'woocommerce-loop-product__title')]//text()").getall()
            part_name = ''.join(part_name).strip()

            # Extract price including currency
            price_parts = card.xpath(".//span[@class='woocommerce-Price-amount amount']/bdi//text()").getall()
            price = ''.join(price_parts).strip()

            # Check for stock status
            in_stock = "yes"  # Default to 'yes'
            out_of_stock_badge = card.xpath(".//span[@class='out-of-stock-badge' and text()='ناموجود']")

            if out_of_stock_badge:
                in_stock = "no"  # Change to 'no' if out of stock

            if part_name and price:
                item = MicromodernItem()
                item['part_name'] = part_name
                item['price'] = price
                item['url'] = response.url
                item['seller'] = "Sisoog"
                item['in_stock'] = in_stock  # Add the in_stock field

                # Set the timestamp with local timezone
                local_tz = pytz.timezone("Asia/Tehran")  # Change this to your desired timezone
                now = datetime.now(local_tz)
                item['date'] = now.date()  # Save date
                item['time'] = now.strftime('%H:%M:%S')  # Save time, cutting precision to seconds

                self.items.append(item)  # Append item to the list

        # Handle pagination
        next_page = response.xpath("//a[@class='next page-numbers']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def close(self, reason):  
        # Create a DataFrame from the scraped items
        new_items = pd.DataFrame([dict(item) for item in self.items])  # Convert list of items to DataFrame

        # Debugging output
        print(f"Total items scraped this run: {len(new_items)}")

        # Prepare the output filenames with a timestamp to avoid overwriting
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_file = f"C:/Users/admin/Desktop/projects/the micro modern project/Data set/time_series_data_sisoog.json"
        excel_file = f"C:/Users/admin/Desktop/projects/the micro modern project/Data set/time_series_data_sisoog.xlsx"

        # Save the new data to JSON
        try:
            new_items.to_json(json_file, orient='records', lines=True, force_ascii=False)
            print(f"JSON file saved successfully: {json_file}")
        except Exception as e:
            print(f"Error saving JSON: {e}")

        # Save the new data to Excel
        try:
            new_items.to_excel(excel_file, index=False)
            print(f"Excel file saved successfully: {excel_file}")
        except Exception as e:
            print(f"Error saving Excel: {e}")