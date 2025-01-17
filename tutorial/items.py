# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class myitem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class ImgItem(scrapy.Item):
	title = scrapy.Field()
	image_urls = scrapy.Field()
	images = scrapy.Field()

class CraigslistSampleItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()