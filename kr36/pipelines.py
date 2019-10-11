# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os


class Kr36Pipeline(object):
    def __init__(self):
        store_file = os.path.dirname(__file__) + '/spiders/36kr.csv'
        self.file = open(store_file, "a+", newline="", encoding="utf_8_sig")
        self.writer = csv.writer(self.file)

    def process_item(self, item, spider):
        try:
            self.writer.writerow((
                item["title"],
                item["app_views_count"],
                item["mobile_views_count"],
                item["views_count"],
                item["column_name"],
                item["favourite_num"],
                item["published_at"],
                item["is_free"],
                item["username"]
            ))
            print("数据存储完毕")
        except Exception as e:
            print(e.args)

    def close_spider(self, spider):
        self.file.close()
