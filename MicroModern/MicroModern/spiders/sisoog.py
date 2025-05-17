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
            
            yield response.follow(url=part_url, callback=self.parse_parts, meta={'part_url': part_url})
            
        next_page = response.xpath("//a[@class='next page-numbers']/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
            
    def parse_parts(self, response):
        item = {
            'seller' : 'sisoog',
            'distributar': 'sisoog',
            'part_url' : response.request.meta['part_url'],
            'part_name': response.xpath("//h1/text()").get(),
            'stock': int(response.xpath("//input[@class='input-text qty text']/@max").get() or 0),
            'bulk_price' : response.xpath("//p[@class='price']/span/bdi/text()").get(),
            'bulk_volume' : '1',
            'historical_date' : date.today(),
            'time' : datetime.now().strftime("%H:%M:%S")
        }
        yield item
