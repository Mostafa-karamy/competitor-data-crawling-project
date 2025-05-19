import scrapy


class MouserSpider(scrapy.Spider):
    name = "mouser"
    allowed_domains = ["mouser.com"]
    search_part = "module"
    start_urls = [f"https://nl.mouser.com/new/{search_part}/n-5g3y"]

    def parse(self, response):
        parts = response.xpath("//table[@id='SearchResultsGrid_grid']/tbody/tr")
        for part in parts:
            part_url = part.xpath(".//td[3]/div[1]/a/@href").get()
            part_ID = part.xpath(".//td[3]/div[2]/span[2]/text()").get()
            # yield response.follow(url=part_url, callback=self.parse_parts, meta={'part_url': part_url,'part_ID':part_ID})
            yield{
                'part url': part_url,
                'part ID': part_ID
            }
        next_page = response.xpath("//ul[@class='pagination']/li/a[@id='lnkPager_lnkNext']/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
