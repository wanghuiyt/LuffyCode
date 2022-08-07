import scrapy
from zhipin.req import SeleniumRequest
from scrapy.http.response.html import HtmlResponse


class BossSpider(scrapy.Spider):
    name = 'boss'
    allowed_domains = ['zhipin.com']
    start_urls = ['https://www.zhipin.com/c101010100/?query=python&page=2&ka=page-2']

    def start_requests(self, ):
        yield SeleniumRequest(url=self.start_urls[0], dont_filter=True)

    def parse(self, resp: HtmlResponse, **kwargs):
        print(resp.text)
