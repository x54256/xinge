# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinanewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    parentTitle = scrapy.Field()
    parentUrls = scrapy.Field()
    subTitle = scrapy.Field()
    subUrls = scrapy.Field()
    child_path = scrapy.Field()
    SonUrl = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()


