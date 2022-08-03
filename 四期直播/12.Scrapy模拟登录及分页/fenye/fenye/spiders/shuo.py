import scrapy
from scrapy.http.response.html import HtmlResponse


class ShuoSpider(scrapy.Spider):
    name = 'shuo'
    allowed_domains = ['17k.com']
    start_urls = ['https://www.17k.com/all/book/2_0_0_0_0_0_0_0_1.html']

    def start_requests(self):
        for i in range(1, 10):
            url = f"https://www.17k.com/all/book/2_0_0_0_0_0_0_0_{i}.html"
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, resp: HtmlResponse, **kwargs):
        # print(resp.text)
        trs = resp.xpath('//table/tbody/tr')
        for tr in trs:
            leibie = tr.xpath('./td[2]//text()').extract()
            name = tr.xpath('./td[3]//text()').extract()
            author = tr.xpath('.//li[@class="zz"]/a/text()').extract_first()
            print(leibie, name, author)
