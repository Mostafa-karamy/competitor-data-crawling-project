import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from time import sleep
from datetime import date, datetime
from scrapy.http import HtmlResponse

class JavanSpider(scrapy.Spider):
    name = "javan"
    allowed_domains = ["www.javanelec.com"]
    search_part = "آنتن"
    def __init__(self, user_input=search_part, *args, **kwargs):
        super(JavanSpider, self).__init__(*args, **kwargs)
        self.user_input = user_input

    def start_requests(self):
        url = f"https://www.javanelec.com/shop?searchfilter={self.user_input}"
        yield SeleniumRequest(url=url, callback=self.scroll_and_parse, wait_time=3)

    def scroll_and_parse(self, response):
        driver = response.meta['driver']
        scroll_increment = 100000
        scroll_pause_time = 4

        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
            sleep(scroll_pause_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        page_source = driver.page_source
        response = HtmlResponse(url=driver.current_url, body=page_source, encoding='utf-8')
        yield from self.parse(response)
        
    def parse(self, response):
        parts = response.xpath("//ul[@id='search_result_content']/li/div/div[1]")
        for part in parts:
            part_url = part.xpath(".//a/@href").get()
            yield response.follow(url=part_url, callback=self.parse_parts, meta={'part_url': part_url})
    
    def parse_parts(self, response):
        part_url = response.meta['part_url']
        part_name = response.xpath("//div[@class='p-03 flex-align-start border-bottom-w']/h1/text()").get()
        product_ID = response.xpath("//div[@id='Product_Detail']/@data-prdid").get()
        StockInfo_link = f'https://www.javanelec.com/shoppingcarts/create?productId={product_ID}'
        
        yield response.follow(url=StockInfo_link,
                              callback=self.parse_stock_info,
                              meta={'part_url': part_url,
                                    'part_name': part_name,})
        
    def parse_stock_info(self, response):
        part_url = response.request.meta['part_url']
        part_name = response.request.meta['part_name']
        bulks = response.xpath('//table[@id="price_quntity"]/tbody/tr')
        
        for bulk in bulks:
            item = {
                'seller' : 'javanelectronic',
                'distributar': 'javanelectronic',
                'part_url': part_url,
                'part_name': (part_name or '').strip(),
                'stock': float(response.xpath('//input[@id="Inventory"]/@value').get() or 0) if bulk else 0,
                'bulk_price' : ((bulk.xpath('.//td[@class="font-weight-bold"]/text()').get() or bulk.xpath(".//td/span/span/text()").get()).strip()) if bulk else 'no stock',
                'bulk_volume' : ((bulk.xpath('.//td/span/text()').get() or '1').strip() or '1') if bulk else 'no stock',
                'historical_date' : date.today(),
                'time' : datetime.now().strftime("%H:%M:%S")
            }
            yield item