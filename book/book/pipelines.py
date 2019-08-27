# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from redis import StrictRedis
from pymongo import *

class BookPipeline(object):
    def open_spider(self, spider):
        client = MongoClient(host='192.168.184.134', port=27017)
        self.db = client.book

    def process_item(self, item, spider):
        """
        :param item: 爬虫提交的 数据对象
        :param spider: 数据来自哪个爬虫
        :return:
        """
        # self.redis_client.set(dict(item))
        self.db.book.insert(dict(item))
        print(item)
        return item
