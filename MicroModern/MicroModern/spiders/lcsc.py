import scrapy
import json
from datetime import date,datetime

class lcscSpider(scrapy.Spider):
    name = "lcsc"
    allowed_domains = ["lcsc.com"]
    search_part = "simcom"
    page_number = 1
    start_urls = [f"https://wmsc.lcsc.com/ftps/wm/search/global?keyword={search_part}&currentPage={page_number}&pageSize=25&searchType=product"]

    def parse(self, response):
        data = json.loads(response.text)
        parts = data.get("result", {}).get("productSearchResultVO", {}).get("productList", [])
        if not parts:
            self.logger.info(f"No products found on page {self.page_number}. Stopping crawl.")
            return  # Stop crawling because no more products
        for part in parts:
            part_url = part.get("url")
            print(part_url)
            stock = part.get('stockNumber')
            print(stock)
            yield response.follow(url=part_url, callback=self.parse_parts, meta={'part_url': part_url,'stock': stock})
        self.page_number += 1
        next_page = f"https://wmsc.lcsc.com/ftps/wm/search/global?keyword={self.search_part}&currentPage={self.page_number}&pageSize=25&searchType=product"
                
        if parts:
            yield scrapy.Request(url=next_page, callback=self.parse)
            
    def parse_parts(self, response):
        part_url = response.request.meta['part_url']
        stock = response.request.meta['stock']
        bulks = response.xpath('(//table[@class="priceTable mt-4"]/tbody)[1]/tr[@class="major2--text"]')
        part_feature = {}
        feature_table = response.xpath("(//div[@class='v-data-table__wrapper'])[1]/table/tbody/tr")
        for feature in feature_table:
            feature_key = feature.xpath(".//td[1]/text()").get().strip()
            feature_value = (feature.xpath(".//td[2]/a/text()").get() or feature.xpath(".//td[2]/text()").get()).strip()
            part_feature[f'{feature_key}'] = feature_value
        for bulk in bulks:
            item = {
                'search_key' : self.search_part,
                'seller' : 'lcsc',
                'distributar': 'lcsc',
                'part_url': part_url,
                'part_ID' : response.xpath("(//td/div[@class='d-flex']/span)[position()=2]/text()").get().strip(),
                'part_name': response.xpath("//h1[@class='font-Bold-600 fz-20']/text()").get().strip(),
                'stock': stock if bulk else 0,
                'bulk_price' : (bulk.xpath('.//td/span/text()').get()) if bulk else 'no stock',
                'bulk_volume' : ((bulk.xpath('.//td/div/span/text()').get() or '1').strip() or '1') if bulk else 'no stock',
                'part_feature': part_feature,
                'historical_date' : date.today(),
                'time' : datetime.now().strftime("%H:%M:%S")
            }
            yield item
