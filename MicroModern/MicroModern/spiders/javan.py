import scrapy
from MicroModern.items import MicromodernItem
from datetime import datetime
import pandas as pd
import os
import pytz

class JavanSpider(scrapy.Spider):
    name = "javan"
    allowed_domains = ["www.javanelec.com"]
    user_input = input('part name: ')
    if user_input == 'all':
        start_urls = ["https://www.javanelec.com/shop"]
    else:
        start_urls = [f"https://www.javanelec.com/shop?searchfilter={user_input}"]

    def __init__(self, *args, **kwargs):
        super(JavanSpider, self).__init__(*args, **kwargs)
        self.items = []  # Initialize a list to hold scraped items

    def parse(self, response):
        # Select product cards based on the provided HTML structure
        product_cards = response.xpath("//li[@data-prdid]")

        if not product_cards:
            self.logger.warning("No product cards found on the page.")
            return

        # Loop through each product card and extract the relevant information
        for card in product_cards:
            # Extract product name
            part_name = card.xpath(".//div[@class='en-num']//div[1]/text()").get().strip()

            # Extract price
            price = card.xpath(".//span[@class='px-01 font-weight-bold']/text()").get()
            price = price.strip() if price else None  # Clean up and handle None

            # Check for stock status
            in_stock = "yes" if price else "no"  # Set to 'yes' if price exists, otherwise 'no'

            # Create an item regardless of stock status
            item = MicromodernItem()
            item['part_name'] = part_name
            item['price'] = price if price else "no stock"#Indicate out of stock in the price field
            item['url'] = response.url
            item['seller'] = "javan"
            item['in_stock'] = in_stock  # Add the in_stock field

            # Set the timestamp with local timezone
            local_tz = pytz.timezone("Asia/Tehran")  # Change this to your desired timezone
            now = datetime.now(local_tz)
            item['date'] = now.date()  # Save date
            item['time'] = now.strftime('%H:%M:%S')  # Save time, cutting precision to seconds

            self.items.append(item)  # Append item to the list

        # Debugging output
        self.logger.info(f"Collected {len(self.items)} items so far.")

    def close(self, reason):
        # Create a DataFrame from the scraped items
        new_items = pd.DataFrame([dict(item) for item in self.items])  # Convert list of items to DataFrame

        # Prepare the output filenames with a timestamp to avoid overwriting
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_file = f"C:/Users/admin/Desktop/projects/the micro modern project/Data set/time_series_data_javan.json"
        excel_file = f"C:/Users/admin/Desktop/projects/the micro modern project/Data set/time_series_data_javan.xlsx"

        # Save the new data to JSON
        try:
            new_items.to_json(json_file, orient='records', lines=True, force_ascii=False)
            self.logger.info(f"JSON file saved successfully: {json_file}")
        except Exception as e:
            self.logger.error(f"Error saving JSON: {e}")

        # Save the new data to Excel
        try:
            new_items.to_excel(excel_file, index=False)
            self.logger.info(f"Excel file saved successfully: {excel_file}")
        except Exception as e:
            self.logger.error(f"Error saving Excel: {e}")


