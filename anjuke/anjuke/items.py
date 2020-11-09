# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CityInfoItem(scrapy.Item):
    # 城市名
    city_name = scrapy.Field()
    # 城市url
    url = scrapy.Field()
    # 城市拼音
    pinyin = scrapy.Field()
    pass


class PriceInfoItem(scrapy.Item):
    # 城市名
    city_name = scrapy.Field()
    month = scrapy.Field()
    trend_type = scrapy.Field()
    trend_rate = scrapy.Field()
    price_des = scrapy.Field()
    price = scrapy.Field()