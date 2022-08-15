# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
import os
from lxml import etree
from scrapy.pipelines.images import ImagesPipeline

class WangxiaoPipeline:
    def process_item(self, item, spider):
        # 内容放到Markdown中，既能保留页面格式，也能保留图片效果
        dir_path = item["dir_path"]
        file_name = item["file_name"]
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        real_path = os.path.join(dir_path, f"{file_name}.md")
        with open(real_path, mode="a", encoding="utf-8") as f:
            f.write("**************************************\n")
            f.write(item["question_info"])
            f.write("\n")
        return item


class WangxiaoImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # 图片的地址
        tree = etree.HTML(item["question_info"])  # type: etree._Element
        srcs = tree.xpath("//img/@src")
        for src in srcs:
            yield scrapy.Request(url=src, dont_filter=True, meta={
                "src": src,
                "dir_path": item["dir_path"],
                "file_name": item["file_name"]
            })

    def file_path(self, request, response=None, info=None, *, item=None):
        # 拼接路径
        dir_path = request.meta["dir_path"]
        file_name = request.meta["file_name"]
        src = request.meta["src"]
        real_file_name = src.split("/")[-1]
        return f"{dir_path}/{file_name}_img/{real_file_name}"

    def item_completed(self, results, item, info):
        # 需要src, 图片真正的存储路径
        # print(results)
        for r in results:
            status = r[0]
            dic = r[1]
            if status:
                url = dic["url"]
                path = dic["path"]
                real_path = "/".join(path.split("/")[-2:])
                item["question_info"] = item["question_info"].replace(url, real_path)
        return item
