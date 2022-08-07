import scrapy
from scrapy.http.response.html import HtmlResponse


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/s?wd=ip']

    def parse(self, resp: HtmlResponse, **kwargs):
        print(resp.text)
