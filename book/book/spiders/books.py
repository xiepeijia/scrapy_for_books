# -*- coding: utf-8 -*-
from functools import reduce

import scrapy
from book.items import BookItem
import re
from retrying import retry
import time


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['sobooks.cc']
    base_urls = "https://sobooks.cc/page/{}"
    pattern = re.compile(r'<h2>内容简介</h2>(.*?)<p><table class="dltable">', re.DOTALL)  # 内容简介提取
    detail_pattern = re.compile(r'>(.*?)<')  # 内容简介数据清洗
    bd_pattern = re.compile(r'url=(.*)')  # 网盘url正则提取
    ct_pattern = re.compile(r'url=(.*)')  # 网盘url正则提取

    def start_requests(self):
        """
        每次引擎想爬虫索要第一个请求会回调这个函数
        给引擎提供首个请求
        :return:
        """
        for page in range(1, 216):

            yield scrapy.Request(
                url=self.base_urls.format(page)

            )

        # yield scrapy.Request(
        #     url = self.base_urls.format(180)
        # )


    def parse(self, response):
        card_list = response.xpath('//div[@class="card-item"]')
        for card in card_list:
            src = card.xpath('.//a[@target="_blank"]/@href').extract_first()
            # item["name"] = card.xpath('.//a[@target="_blank"]/text()').extract_first()
            # item["img_src"] = card.xpath('.//img/@src')

            yield scrapy.Request(
                url=src,
                callback=self.parse_detail,
            )


    def parse_detail(self, response):

        book = BookItem()
        book["name"] = response.xpath('//strong[text()="书名："]/../text()').extract_first()
        book["author"] = response.xpath('//strong[text()="作者："]/../text()').extract_first()
        book["target"] = response.xpath('//strong[text()="标签："]/../a/text()').extract()
        book["time"] = response.xpath('//strong[text()="时间："]/../text()').extract_first()
        book["ISBN"] = response.xpath('//strong[text()="ISBN："]/../text()').extract_first()
        book["publish"] = response.xpath('//strong[text()="出版社："]/../text()').extract_first()
        book["img_url"] = response.xpath('//div[@class="bookpic"]/img/@src').extract_first()

        baidu_nd = response.xpath('//a[text()="百度网盘"]/@href').extract_first()
        chengtong_nd = response.xpath('//a[text()="城通网盘（备用）"]/@href').extract_first()
        if baidu_nd != None:
            book["baidu_nd"] = self.bd_pattern.findall(baidu_nd)[0]
        else:
            book["baidu_nd"] = ""
        if chengtong_nd != None:
            book["chengtong_nd"] = self.ct_pattern.findall(chengtong_nd)[0]
        else:
            book["chengtong_nd"] = ""

        base_content = self.pattern.findall(response.text)
        if base_content:
            detail_list = self.detail_pattern.findall(base_content[0])
            book["content_intro"] = "内容简介:" + reduce(lambda x, y: x + y, detail_list)
        else:
            book["content_intro"] = None
        # print(response.text)
        yield book
