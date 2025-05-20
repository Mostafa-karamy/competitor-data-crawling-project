import scrapy
from datetime import date, datetime

class DigipartSpider(scrapy.Spider):
    name = "digipart"
    allowed_domains = ["www.digipart.com"]
    search_part = 'sim800'
    start_urls = [f"https://www.digipart.com/part/{search_part}"]

    def parse(self, response):
        distributors = response.xpath("//div[@id='stock-container']/div")
        
        for distributor in distributors:
            distributor_name = distributor.xpath(".//div/a/div/text()").get()
            
            if distributor_name:
                distributor_name = distributor_name.strip()
                
            parts = distributor.xpath(".//div[@class='div-rst-tbl']/table/tbody/tr")
            
            for part in parts:
                part_name = part.xpath(".//td[@class='td-mpn']/a/text()").get()
                part_url = part.xpath(".//td[@class='td-mpn']/a/@href").get()
                stock = part.xpath(".//td[@class='td-stock']/text()").get()
                part_name = part_name.strip() if part_name else ''
                part_url = part_url.strip() if part_url else ''
                stock = stock.strip() if stock else 'unknown'
                bulks_boxes = part.xpath(".//td[@class='td-price']")
                
                for bulk_box in bulks_boxes:
                    bulks = bulk_box.xpath(".//table/tr")
                    
                    for bulk in bulks:
                        bulk_price = (bulk.xpath(".//td[@class='prc-brk']/text()").get() or 
                                      bulk.xpath(".//td[@style='text-align:right']/text()").get())
                        bulk_volume = bulk.xpath(".//td[@class='qty-brk']/text()").get()
                        item = {
                            'search_key' : self.search_part,
                            'seller': 'digipart',
                            'distributor': distributor_name,
                            'part_url': part_url,
                            'part_ID' : '',
                            'part_name': part_name,
                            'stock': stock,
                            'bulk_price': bulk_price.strip() if bulk_price else 'no price',
                            'bulk_volume': (bulk_volume.strip() if bulk_volume else "1") if bulk_price else "no volume",
                            'part_feature' : {},
                            'historical_date': date.today(),
                            'time': datetime.now().strftime("%H:%M:%S")
                        }
                        if bulk_price:
                            yield item
                        else:
                            pass
