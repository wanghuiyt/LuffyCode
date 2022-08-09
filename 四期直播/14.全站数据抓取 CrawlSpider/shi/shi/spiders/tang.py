import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TangSpider(CrawlSpider):
    name = 'tang'
    allowed_domains = ['shicimingjv.com']
    start_urls = ['https://www.shicimingjv.com/tangshi/index_1.html']

    # 省略了parse
    rules = (
        # 自动提取链接，并发送请求
        Rule(LinkExtractor(restrict_xpaths="//div[@class='sec-panel-body']/ul/li/div/h3"), callback='parse_item'),
        # follow:表示是否继续重新来一遍 => 相当于前面案例中的callback=self.parse
        # 能够拿到 2.html 3.html 4.html ...
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='pagination']/li/a"), follow=True),
    )

    # CrawlSpider的执行过程
    # def parse(self, resp: HtmlResponse, **kwargs):
    #     for r in self.rules:
    #         links = r.link_extractor.extract_links(resp)
    #         for link in links:
    #             url = link.url
    #             yield scrapy.Request(url=url, callback=r.callback)

    def parse_item(self, response: HtmlResponse, **kwargs):
        # item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        # return item

        # 解析详情页的信息
        title = response.xpath('//h1[@class="mp3"]/text()').extract_first()
        print(title)


