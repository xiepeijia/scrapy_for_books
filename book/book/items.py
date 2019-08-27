# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    target = scrapy.Field()
    url = scrapy.Field()
    img_url = scrapy.Field()
    time = scrapy.Field()
    ISBN = scrapy.Field()
    publish = scrapy.Field()
    content_intro = scrapy.Field()
    baidu_nd = scrapy.Field()
    chengtong_nd = scrapy.Field()



    pass
