import scrapy
from datetime import date,datetime
import os
import pytz

class SisoogSpider(scrapy.Spider):
    name = "sisoog"
    allowed_domains = ["shop.sisoog.com"]
    search_part = "آنتن"
    start_urls = [f"https://shop.sisoog.com/products/?s={search_part}"]



    def parse(self, response):
        parts = response.xpath("//ul[@class='products columns-3']/li")
        for part in parts:
            part_url = part.xpath(".//a/@href").get()
            part_ID = part.xpath(".//div/a/@data-product_id").get()
            yield response.follow(url=part_url, callback=self.parse_parts, meta={'part_url': part_url,'part_ID':part_ID})
            
        next_page = response.xpath("//a[@class='next page-numbers']/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
            
    def parse_parts(self, response):
        # with open("debug.html", "w", encoding='utf-8') as f:
        #     f.write(response.text)
        part_url = response.request.meta['part_url']
        part_ID = response.request.meta['part_ID']
        part_feature = {}
        feature_table = response.xpath("//table[@class='woocommerce-product-attributes shop_attributes']/tr")
        for feature in feature_table:
            feature_key = feature.xpath(".//th/text()").get().strip()
            feature_value = feature.xpath(".//td/p/text()").get().strip()
            part_feature[f'{feature_key}'] = feature_value
            
        item = {
            'search_key' : self.search_part,
            'seller' : 'sisoog',
            'distributar': 'sisoog',
            'part_url' : part_url,
            'part_ID': part_ID,
            'part_name': response.xpath("//h1/text()").get(),
            'stock': int(response.xpath("//input[@class='input-text qty text']/@max").get() or 0),
            'bulk_price' : response.xpath("//p[@class='price']/span/bdi/text()").get(),
            'bulk_volume' : '1',
            'part_feature': part_feature,
            'historical_date' : date.today(),
            'time' : datetime.now().strftime("%H:%M:%S")
        }
        yield item
