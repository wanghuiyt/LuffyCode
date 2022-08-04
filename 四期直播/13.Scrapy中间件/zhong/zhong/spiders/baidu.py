import scrapy
from scrapy.http.response.html import HtmlResponse


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    start_urls = ['http://www.baidu.com/']  # 避免重定向

    def parse(self, resp: HtmlResponse, **kwargs):
        print(resp.url)
