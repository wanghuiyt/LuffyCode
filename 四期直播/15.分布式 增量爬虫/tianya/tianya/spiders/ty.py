import scrapy
from redis import Redis
from scrapy import signals
from scrapy.http.response.html import HtmlResponse


class TySpider(scrapy.Spider):
    name = 'ty'
    allowed_domains = ['tianya.cn']
    start_urls = ['http://bbs.tianya.cn/list.jsp?item=free&order=1']

    """
    需要redis来去除重复的url
    先打开redis，创建好连接
    """
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_opened(self, spider):
        self.redis = Redis(
            host="127.0.0.1",
            port=6379,
            password="123456",
            db=6,
            decode_responses=True
        )

    def spider_closed(self, spider):
        if self.redis:
            self.redis.close()

    def parse(self, resp: HtmlResponse, **kwargs):
        tbodys = resp.xpath('//div[@class="mt5"]/table/tbody')[1:]
        for tbody in tbodys:
            trs = tbody.xpath('./tr')
            for tr in trs:
                href = tr.xpath('./td[1]/a/@href').extract_first()
                href = resp.urljoin(href)
                # 判断是否已经抓取过了，如果已经抓取过了，不再重复抓取了
                # 没有抓取过，就发送请求，并添加到redis中
                if self.redis.sismember("ty:urls", href):
                    continue
                else:
                    # 在这里添加到redis中，不太安全，有可能会请求失败
                    yield scrapy.Request(url=href, callback=self.parse_detail, meta={"href": href})

        """
        如果要分页，需要给出一个边界
        先找到下一页的链接
        hh = "xxxx"
        if int(resp.meta["page"]) <= 3:
            yield scrapy.Request(url=hh, callback=self.parse, meta={"page": 变量})
        """

    def parse_detail(self, resp: HtmlResponse, **kwargs):
        contents = resp.xpath('//div[@class="bbs-content clearfix"]//text()').extract()
        content = "".join(contents)
        content = content.strip()

        # url去重
        # href = resp.meta["href"]  # 一定要手工传递过来，防止重定向发生
        # self.redis.sadd("ty:urls", href)

        # 数据去重
        yield {"content": content}
