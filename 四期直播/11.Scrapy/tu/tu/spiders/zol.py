import scrapy
# from urllib.parse import urljoin
from scrapy.http.response.html import HtmlResponse


class ZolSpider(scrapy.Spider):
    name = 'zol'
    allowed_domains = ['zol.com.cn']
    start_urls = ['https://desk.zol.com.cn/dongman/']

    def parse(self, resp: HtmlResponse, **kwargs):
        # print(resp.text)
        # 1.拿到性情页的url
        a_list = resp.xpath('//*[@class="pic-list2  clearfix"]/li/a')
        for a in a_list:
            href = a.xpath('./@href').extract_first()
            if href.endswith(".exe"):
                continue
            # href = urljoin(self.start_urls[0], href)
            # href = urljoin(resp.url, href)  # resp.url: 当前这个响应是请求的哪个url返回的
            href = resp.urljoin(href)
            # print(href)
            # 2.请求详情页，拿到图片的下载地址
            """
            发送一个新的请求
            返回一个新的请求对象
            我们需要在请求对象中，给出至少以下内容(scrapy中)
            url:请求url
            method：请求方式
            data：参数
            callback：请求成功得到响应之后，如何解析(parse),把解析函数名字放进去
            """
            yield scrapy.Request(
                url=href,
                method="get",
                callback=self.parse_detail  # 当url返回之后，自动执行的那个解析函数
            )

    def parse_detail(self, resp: HtmlResponse, **kwargs):
        # 在这里得到的响应，就是url=href返回的响应
        img_src = resp.xpath('//*[@id="bigImg"]/@src').extract_first()
        # print(img_src)
        yield {"img_src": img_src}

