import scrapy
from ..items import CaiItem
from scrapy.http.response.html import HtmlResponse


class SsqSpider(scrapy.Spider):
    name = 'ssq'
    allowed_domains = ['sina.com.cn']
    start_urls = ['https://match.lottery.sina.com.cn/lotto/pc_zst/index?lottoType=ssq&actionType=chzs']

    def parse(self, resp: HtmlResponse, **kwargs):
        # print(resp.text)
        # 解析出你需要的数据
        trs = resp.xpath('//*[@id="cpdata"]/tr')
        for tr in trs:
            red_ball = tr.xpath('./td[@class="chartball01" or @class="chartball20"]/text()').extract()
            if not red_ball:
                continue
            blue_ball = tr.xpath('./td[@class="chartball02"]/text()').extract_first()
            qi = tr.xpath('./td[1]/text()').extract_first()
            # print(qi, red_ball, blue_ball)
            # 官方推荐使用Item来约束数据结构，提前定义这个结构
            item = CaiItem()
            item["qi"] = qi
            item["red_ball"] = '_'.join(red_ball)
            item["blue_ball"] = blue_ball
            yield item
