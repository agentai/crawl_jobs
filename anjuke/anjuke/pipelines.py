# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonLinesItemExporter as ItemExporter
from anjuke.items import CityInfoItem, PriceInfoItem
import time


class AnjukePipeline:

    def open_spider(self, spider):
        self.file_city = open("city.json_{}".format(int(time.time())), "wb")
        self.exporter_city = ItemExporter(self.file_city, encoding="utf8")
        self.exporter_city.start_exporting()

        self.file_price = open("price.json_{}".format(int(time.time())), "wb")
        self.exporter_price = ItemExporter(self.file_price, encoding="utf8")
        self.exporter_price.start_exporting()

    def process_item(self, item, spider):
        if type(item) == CityInfoItem:
            self.exporter_city.export_item(item)
        if type(item) == PriceInfoItem:
            self.exporter_price.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter_city.finish_exporting()
        self.exporter_price.finish_exporting()
        self.file_city.close()
        self.file_price.close()
