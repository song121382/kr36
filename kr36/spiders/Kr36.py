# -*- coding: utf-8 -*-
import scrapy
import json

from scrapy import Request

from kr36.items import Kr36Item


class Kr36Spider(scrapy.Spider):
    name = 'Kr36'
    allowed_domains = ['36kr.com']
    start_urls = ['https://36kr.com/api/search-column/mainsite?per_page=100&page=1&_=']

    def parse(self, response):
        data = json.loads(response.body_as_unicode())
        total = int(data["data"]["total_count"])

        for page in range(2, int(total / 100) + 2):
            print("正在爬取{}页".format(page), end="")
            yield Request("https://36kr.com/api/search-column/mainsite?per_page=100&page={}&_=".format(str(page)), callback=self.parse_item)

    def parse_item(self, response):
        data = json.loads(response.body_as_unicode())
        item = Kr36Item()
        for one_item in data["data"]["items"]:
            print(one_item)
            item["app_views_count"] = one_item["app_views_count"] if "app_views_count" in one_item else 0  # APP观看数量
            item["mobile_views_count"] = one_item[
                "mobile_views_count"] if "mobile_views_count" in one_item else 0  # 移动端观看数量
            item["views_count"] = one_item["views_count"] if "views_count" in one_item else 0  # PC观看数量
            item["column_name"] = one_item["column_name"]  # 类别
            item["favourite_num"] = one_item["favourite_num"] if "favourite_num" in one_item else 0  # 收藏数量
            item["title"] = one_item["title"]  # 标题
            item["published_at"] = one_item["published_at"]  # 发布时间
            item["is_free"] = one_item["is_free"] if "is_free" in one_item else 0  # 是否免费
            item["username"] = json.loads(one_item["user_info"])["name"]
            yield item