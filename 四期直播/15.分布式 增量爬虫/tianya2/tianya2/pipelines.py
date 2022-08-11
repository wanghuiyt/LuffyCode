# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from redis import Redis


class Tianya2Pipeline:
    def open_spider(self, spider):
        self.redis = Redis(
            host="127.0.0.1",
            port=6379,
            password="123456",
            db=6
        )

    def close_spider(self, spider):
        if self.redis:
            self.redis.close()

    def process_item(self, item, spider):
        content = item["content"]
        if self.redis.sismember("ty:content", content):
            print("已经存在了，不需要重复存储")
        else:
            self.redis.sadd("ty:content", content)
        return item
