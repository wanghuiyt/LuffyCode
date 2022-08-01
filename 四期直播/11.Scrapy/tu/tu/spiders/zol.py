import scrapy
# from urllib.parse import urljoin
from scrapy.http.response.html import HtmlResponse


class ZolSpider(scrapy.Spider):
    name = 'zol'
    allowed_domains = ['zol.com.cn']
    start_urls = ['https://desk.zol.com.cn/dongman/']

    def parse(self, resp: HtmlResponse, **kwargs):
        print(resp.text)
        # 1.拿到性情页的url
        a_list = resp.xpath('//*[@class="pic-list2  clearfix"]/li/a')
        for a in a_list:
            href = a.xpath('./@href').extract_first()
            if href.endswith(".exe"):
                continue
            # href = urljoin(self.start_urls[0], href)
            # href = urljoin(resp.url, href)  # resp.url: 当前这个响应是请求的哪个url返回的
            href = resp.urljoin(href)
            print(href)
        # 2.请求详情页，拿到图片的下载地址
