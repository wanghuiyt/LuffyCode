import scrapy
from scrapy.http.response.html import HtmlResponse

# 提前定义数据结构
che_label = {
    "表显里程": "licheng",
    "上牌时间": "shijian",
    "挡位/排量": "pailiang",
    "车辆所在地": "suozaidi",
    "查看限迁地": "biaozhun",
}


class JiaSpider(scrapy.Spider):
    name = 'jia'
    allowed_domains = ['che168.com']
    start_urls = ['https://www.che168.com/beijing/a0_0msdgscncgpi1ltocsp1exx0/']

    def parse(self, resp: HtmlResponse, **kwargs):
        # print(resp.url)  # 做个测试，验证请求是通的
        li_list = resp.xpath('//ul[@class="viewlist_ul"]/li')
        for li in li_list:
            href = li.xpath('./a/@href').extract_first()
            href = resp.urljoin(href)
            # 过滤广告
            if "topicm" in href:
                continue
            # print(href)
            # 发请求
            """
            请求1  请求2  请求3
            在请求2被yield的时候，请求1一定回来了吗？
            不一定回来了，只能说明请求给了引擎，后续的操作是否完成谁也不知道，只能在parse_detail中可以看得出来，回来的顺序也不确定
            """
            yield scrapy.Request(
                url=href,
                callback=self.parse_detail
            )
        # 分页逻辑 在这里被执行的时候
        print("我爱你")
        hrefs = resp.xpath('//div[@id="listpagination"]/a/@href').extract()
        for href in hrefs:
            if href.startswith("javascript"):
                continue
            href = resp.urljoin(href)
            # print(href)
            # 每一页都走一遍第一页的流程
            yield scrapy.Request(
                url=href,
                callback=self.parse
            )

    def parse_detail(self, resp: HtmlResponse, **kwargs):
        # 这里能被执行，说明对详情页的请求回来了
        # 解析详情页的内容
        name = resp.xpath('//*[@class="car-box"]/h3/text()').extract_first()
        if not name:
            return
        print(name.strip())
        li_list = resp.xpath('//div[@class="car-box"]/ul/li')
        dic = {
            'licheng': '0公里',
            'shijian': '未知',
            'pailiang': '未知',
            'suozaidi': '地球',
            'biaozhun': '未知'
        }
        # 可以考虑给出字典的默认值，找defaultDict或者手动给出默认值
        for li in li_list:
            p_name = li.xpath('./p//text()').extract_first()
            p_value = li.xpath('./h4/text()').extract_first()
            # print(p_name, p_value)
            p_name = p_name.replace(" ", "").strip()
            p_value = p_value.strip()
            data_key = che_label.get(p_name)
            dic[data_key] = p_value
        print(dic)
        yield dic

        # 考虑分页
        # 1.拿urls
        # for u in urls:
        #    yield scrapy.Request(url=u, callback=self.parse_detail)

