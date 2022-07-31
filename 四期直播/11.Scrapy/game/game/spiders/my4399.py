import scrapy
from scrapy.http.response.html import HtmlResponse


class My4399Spider(scrapy.Spider):
    name = 'my4399'
    # 限制该spider抓取的域名，只要不符合该域名的一概过掉
    allowed_domains = ['4399.com']
    """
    起始url，在引擎开始工作的时候，自动的包装成一个请求对象
    引擎进行调度，交给下载器获取页面源代码，帮你封装成响应对象
    引擎把响应对象交给spider进行解析，解析函数就是下面的parse
    """
    start_urls = ['http://www.4399.com/flash/game100.htm']

    """
    解析start_url返回的响应
    函数名不能乱改
    参数**kwargs，根据自己的喜好进行增加 # 形参 => 变量
    不是自己调用的，是引擎自动调用，参数也是引擎自动传递
    """
    def parse(self, resp: HtmlResponse):
        # print(resp.text)
        # 插曲：去settings.py中设置 LOG_LEVEL ROBOTSTXT_OBEY
        """
        以前的做法
        from lxml import etree
        tree = etree.HTML(resp.text)
        tree.xpath("xxx")
        """
        li_list = resp.xpath('//*[@id="list"]/li')
        for li in li_list:
            # extract() 是提取内容的，但是需要取[0]，存在风险
            # extract_first() 提取第一个，好处是不会越界，如果没有东西，这里获取到的是None
            # name = li.xpath('./div[1]/a//text()').extract()[0]
            name = li.xpath('./div[1]/a//text()').extract_first()
            if not name:
                continue
            leibie = li.xpath("./span[1]/a/text()").extract_first()
            if not leibie:
                continue
            shijian = li.xpath("./span[2]/text()").extract_first()
            if not leibie:
                continue
            # print(name, leibie, shijian)
            """
            只能返回以下内容：
            dict item  # 是数据，去pipeline保存数据
            request  # 继续请求，去调度器的请求队列
            None  # 结束
            """
            yield {"name": name, "leibie": leibie, "shijian": shijian}