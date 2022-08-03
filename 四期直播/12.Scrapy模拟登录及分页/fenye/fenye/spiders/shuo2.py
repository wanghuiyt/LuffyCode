import scrapy
from scrapy.http.response.html import HtmlResponse


class Shuo2Spider(scrapy.Spider):
    name = 'shuo2'
    allowed_domains = ['17k.com']
    start_urls = ['https://www.17k.com/all/book/2_0_0_0_0_0_0_0_1.html']

    def parse(self, resp: HtmlResponse, **kwargs):
        trs = resp.xpath('//table/tbody/tr')
        for tr in trs:
            leibie = tr.xpath('./td[2]//text()').extract()
            name = tr.xpath('./td[3]//text()').extract()
            author = tr.xpath('.//li[@class="zz"]/a/text()').extract_first()
            # print(leibie, name, author)
            yield {"leibie": leibie, "name": name, "author": author}
        # 在解析完数据之后，可以提取分页的url？
        print("开始解析下一页")
        hrefs = resp.xpath('//div[@class="page"]/a/@href').extract()
        for href in hrefs:
            if href.startswith("javascript"):
                continue
            href = resp.urljoin(href)
            print(href)
            # 发送新的请求到2，3，4，5，6
            # scrapy中的调度器 有一个set集合，会去除重复的url,把不重复的放到请求队列中，跑完就自动结束了
            yield scrapy.Request(
                url=href,  # 2,3,4,5,6的结果和1一样，那么解析的时候，是不是一样的的逻辑？
                callback=self.parse,  # 交给引擎调度，不是递归
                # dont_filter=True  # 不去重
            )