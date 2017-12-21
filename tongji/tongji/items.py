# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TongjiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sheng = scrapy.Field()
    shi= scrapy.Field()
    shibianma = scrapy.Field()
    quxian = scrapy.Field()
    quxianbianma = scrapy.Field()
    jiedao = scrapy.Field()
    jiedaobianma = scrapy.Field()
    weiyuanhui = scrapy.Field()
    weiyuanhuibianma = scrapy.Field()


