#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : chitao
# @Time    : 2020/11/5 11:42 上午
# @Email   : chitao@staff.weibo.com

"""
文件说明：
    
"""



import scrapy
import json

from anjuke.items import CityInfoItem, PriceInfoItem


class FangjiaSpider(scrapy.Spider):
    name = 'anjuke_city'
    allowed_domains = ['anjuke.com']
    start_urls = ['https://www.anjuke.com/sy-city.html']

    def parse(self, response):
        years = [str(i) for i in range(2018, 2021)]
        fangjia_base_url = "https://www.anjuke.com/fangjia/{}{}/"
        city_infos = {}
        city_paths = response.xpath("//div[@class='city_list']//a")
        for city_path in city_paths:
            city_info = {
                "city_name": city_path.xpath(".//text()").get().strip(),
                "url": city_path.xpath(".//@href").get().strip(),
            }
            city_info["pinyin"] = city_info["url"].split(".anjuke")[0].replace("https://", "")
            city_info["fangjia_url"] = [fangjia_base_url.format(city_info["pinyin"], year) for year in years]

            city_info_item = CityInfoItem(
                city_name=city_info["city_name"], url=city_info["url"], pinyin=city_info["pinyin"]
            )
            yield city_info_item

            city_infos[city_info["city_name"]] = city_info
            for fangjia_url in city_info["fangjia_url"]:
                yield scrapy.Request(url=fangjia_url, callback=self.parse_fangjia, meta=city_info)
                # break
            # break
        print("city_size", len(city_infos))

    def parse_fangjia(self, response):
        city_info = response.meta
        print("start", city_info["city_name"], response.url)
        price_path_list = response.xpath('//div[@class="fjlist-box boxstyle2"]')[0].xpath('.//li')
        for price_path in price_path_list:
            trend_type = price_path.xpath("@class").get().strip().split(" ")[1]
            month = price_path.xpath(".//a//b//text()").get().strip().replace("房价", "")
            price_des = price_path.xpath(".//a//span//text()").get().strip()
            price = price_path.xpath(".//a//span//text()").get().strip().replace("元/㎡", "")
            trend_rate = price_path.xpath(".//a//em//text()").get().strip()
            if trend_rate== "--":
                trend_rate = float("0.0")
            else:
                trend_rate = float(trend_rate.split("%")[0])
            price_info_item = PriceInfoItem(
                city_name=city_info["city_name"],
                price=price, price_des=price_des,
                trend_type=trend_type, trend_rate=trend_rate,
                month=month
            )
            yield price_info_item
        print("done", city_info["city_name"], response.url)


