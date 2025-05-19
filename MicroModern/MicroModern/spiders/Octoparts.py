import scrapy


class OctopartsSpider(scrapy.Spider):
    name = "Octoparts"
    allowed_domains = ["octopart.com"]
    search_part = "sim800"
    start_urls = [f"https://octopart.com/search?q={search_part}&currency=USD&specs=0"]

    def parse(self, response):
        parts = response.xpath("//div[@class='bg-white pb-3']")
        for part in parts:
            part_url = part.xpath(".//div/div/div/div/div/a/@href").get()
            part_ID = part.xpath(".//@id").get()
            yield{
                'part_url': part_url,
                'part ID': part_ID
            }
            
        next_page = response.xpath("//nav[@class='mt-[22px] flex justify-center']/a/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
