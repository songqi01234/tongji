# -*- coding: utf-8 -*-
import re
import scrapy
from copy import deepcopy
from scrapy_redis.spiders import RedisSpider


class A11Spider(RedisSpider):
    name = 'tongji_spider'
    allowed_domains = ['www.stats.gov.cn']
    # start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/']
    start_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/'
    redis_key = "start"

    # 省
    def parse(self, response):
        td_list = response.xpath('//tr[@class="provincetr"]/td')
        for td in td_list:
            item = {}
            item['sheng'] = td.xpath('./a/text()').extract_first()
            # print(item['sheng'])
            shi_urls = td.xpath('./a/@href').extract_first()
            shi_url = self.start_url + shi_urls
            # print(shi_url)
            yield scrapy.Request(
                shi_url,
                callback=self.parse_shi,
                meta={'item': item}
            )

    # 市及编码
    def parse_shi(self, response):
        item = response.meta['item']
        tr_list = response.xpath('//tr[@class="citytr"]')
        for tr in tr_list:
            item['shi'] = tr.xpath('./td[2]/a/text()').extract_first()
            # print(item['shi'])
            # 获取区县url
            item['shibianma'] = tr.xpath('./td[1]/a/text()').extract_first()
            qu_urls = tr.xpath('./td[1]/a/@href').extract_first()
            qu_url = self.start_url + qu_urls
            yield scrapy.Request(
                qu_url,
                callback=self.parse_qu,
                meta={'item': deepcopy(item)}
            )

    # 区县及编码
    def parse_qu(self, response):
        urls = response.url
        item = response.meta['item']
        tr_list = response.xpath('//tr[@class="countytr"]')
        for tr in tr_list:
            item['quxian'] = tr.xpath('./td[2]/a/text()').extract_first()
            if item['quxian'] is None:
                item['quxian'] = None
            item['quxianbianma'] = tr.xpath('./td[1]/a/text()').extract_first()
            # 构造街道url
            jiedao_urls = tr.xpath('./td[1]/a/@href').extract_first()
            # print(jiedao_urls)
            if jiedao_urls is not None:
                jiedao_url1 = re.findall(r'(http.*?/)\d+.html', urls, re.S)
                for i in jiedao_url1:
                    jiedao_url = i + jiedao_urls
                    # print(jiedao_url)
                    yield scrapy.Request(
                        jiedao_url,
                        callback=self.parse_jiedao,
                        meta={'item': deepcopy(item)}
                    )

    # 街道及编码
    def parse_jiedao(self, response):
        urls = response.url
        item = response.meta['item']
        tr_list = response.xpath('//tr[@class="towntr"]')
        for tr in tr_list:
            item['jiedao'] = tr.xpath('./td[2]/a/text()').extract_first()
            item['jiedaobianma'] = tr.xpath('./td[1]/a/text()').extract_first()
            # 构造委员会url
            weiyuanhui_urls = tr.xpath('./td[2]/a/@href').extract_first()
            weiyuanhui_url1 = re.findall(r'(http.*?/)\d+.html', urls, re.S)
            for i in weiyuanhui_url1:
                weiyuanhui_url = i + weiyuanhui_urls
                yield scrapy.Request(
                    weiyuanhui_url,
                    callback=self.parse_weiyuanhui,
                    meta={'item': deepcopy(item)}
                )

    # 委员会及编码
    def parse_weiyuanhui(self, response):
        print('正在请求', response.url)
        item = response.meta['item']
        tr_list = response.xpath('//tr[@class="villagetr"]')
        for tr in tr_list:
            item['weiyuanhui'] = tr.xpath('./td[3]/text()').extract_first()
            item['weiyuanhuibianma'] = tr.xpath('./td[1]/text()').extract_first()
            yield item
            # print(item)
