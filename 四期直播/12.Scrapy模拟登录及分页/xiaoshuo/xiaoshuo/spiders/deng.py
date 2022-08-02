import scrapy
from scrapy.http.response.html import HtmlResponse


class DengSpider(scrapy.Spider):
    name = 'deng'
    allowed_domains = ['17k.com']
    start_urls = ['https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919']

    def parse(self, resp: HtmlResponse, **kwargs):
        print(resp.text)
