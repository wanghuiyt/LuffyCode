# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import pymongo


# 存文件
class CaiPipeline:
    # 希望程序在跑起来的时候，打开一个w模式的文件
    # 在获取数据的时候正常写入
    # 在程序结束的时候关闭

    # 仅限pipeline，固定写法
    # 爬虫开始的时候执行
    def open_spider(self, spider):
        # print(spider.name)
        self.f = open("data.csv", mode="w", encoding="utf-8")

    # 爬虫结束的时候执行
    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):
        # print("这是管道 ", item)
        # 存储数据：文件，MySQL，mongodb，redis
        self.f.write(item['qi'])
        self.f.write(',')
        self.f.write('_'.join(item['red_ball']))
        self.f.write(',')
        self.f.write(item['blue_ball'])
        self.f.write('\n')
        return item


# 存mysql
class MySQLPipeline:
    def open_spider(self, spider):
        # 连接MySQL
        self.conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            database="luffy",
            user="root",
            password="root"
        )
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        # 关闭连接
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        # 存储数据
        try:
            qi = item["qi"]
            red_ball = "_".join(item["red_ball"])
            blue_ball = item["blue_ball"]
            sql = f"insert into ssq(qi,red_ball,blue_ball) values('{qi}', '{red_ball}', '{blue_ball}')"
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return item


class MongoPipeline:
    def open_spider(self, spider):
        self.conn = pymongo.MongoClient(host="localhost", port=27017)
        self.db = self.conn["python_3"]


    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.db.ssq.insert_one(item)
        return item