import scrapy
from redis import Redis
from scrapy import signals
from scrapy.http.response.html import HtmlResponse
from scrapy_redis.spiders import RedisSpider


class Ty2Spider(RedisSpider):
    """
    安装scrapy-redis
    1.改造spider
    """
    name = 'ty2'
    allowed_domains = ['tianya.cn']
    # start_urls = ['http://bbs.tianya.cn/list.jsp?item=free&order=1']
    # 2.准备启动url
    redis_key = "ty2:urls"

    def parse(self, resp: HtmlResponse, **kwargs):
        tbodys = resp.xpath('//div[@class="mt5"]/table/tbody')[1:]
        for tbody in tbodys:
            trs = tbody.xpath('./tr')
            for tr in trs:
                href = tr.xpath('./td[1]/a/@href').extract_first()
                href = resp.urljoin(href)
                yield scrapy.Request(url=href, callback=self.parse_detail, meta={"href": href})

    def parse_detail(self, resp: HtmlResponse, **kwargs):
        contents = resp.xpath('//div[@class="bbs-content clearfix"]//text()').extract()
        content = "".join(contents)
        content = content.strip()
        print(content)
        yield {"content": content}

    # 程序启动的时候，可以直接从redis走
    # 访问第一个url=》一堆详情页的url=》进入redis list做队列
    # 成功的请求到详情页的url数据处理完毕之后，可以从redis中删除掉该url
