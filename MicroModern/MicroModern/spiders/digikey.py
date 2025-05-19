import scrapy


class DigikeySpider(scrapy.Spider):
    name = "digikey"
    allowed_domains = ["www.digikey.com"]
    start_urls = ["http://www.digikey.com/"]

    def parse(self, response):
        pass
