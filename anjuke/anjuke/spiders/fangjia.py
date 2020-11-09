#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : chitao
# @Time    : 2020/11/4 5:39 下午
# @Email   : chitao@staff.weibo.com

"""
文件说明：

"""

import scrapy
import json


class FangjiaSpider(scrapy.Spider):
    name = 'anjuke_fangjia'
    allowed_domains = ['anjuke.com']
    start_urls = ['http://www.anjuke.com/fangjia']

    def parse(self, response):
        city_infos = {}
        city_paths = response.xpath("//span[@class='elem-l']//a")
        for city_path in city_paths:
            city_info = {
                "city_name": city_path.xpath(".//text()").get().strip(),
                "url": city_path.xpath(".//@href").get().strip(),
            }
            print(json.dumps(city_info, ensure_ascii=False))
            city_infos[city_info["city_name"]] = city_info
        print(json.dumps(city_infos, ensure_ascii=False))
        pass
