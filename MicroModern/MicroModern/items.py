# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MicromodernItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    part_name = scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    seller = scrapy.Field()
    time = scrapy.Field()
    date = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    in_stock = scrapy.Field()