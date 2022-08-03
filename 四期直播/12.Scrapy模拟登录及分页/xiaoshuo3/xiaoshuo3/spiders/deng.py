import scrapy
from scrapy.http.response.html import HtmlResponse


class DengSpider(scrapy.Spider):
    name = 'deng'
    allowed_domains = ['17k.com']
    start_urls = ['https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919']

    # 需要先登录，登录完成之后，才开始start_urls
    def start_requests(self):
        # 完成登录操作
        # scrapy想要发送POST请求：两种方式
        login_url = "https://passport.17k.com/ck/user/login"
        # 参数：loginName:16538989670 password:q6035945

        # 发送post请求，方案一
        # yield scrapy.Request(
        #     url=login_url,
        #     method="POST",
        #     body="loginName=16538989670&password=q6035945",  # 注意，这里要求body是字符串
        #     callback=self.login_success
        # )

        # 发送post请求，方案二
        yield scrapy.FormRequest(
            url=login_url,
            method="POST",
            formdata={
                "loginName": "16538989670",
                "password": "q6035945"
            },
            callback=self.login_success
        )

    def login_success(self, resp: HtmlResponse, **kwargs):
        print(resp.text)
        # 登录成功之后，需要请求到start_urls里面, 不需要手工去处理cookie
        yield scrapy.Request(url=self.start_urls[0], dont_filter=True, callback=self.parse)

    def parse(self, resp: HtmlResponse, **kwargs):
        print(resp.text)

    # 总结，在scrapy中，只要你需要发送请求了，写yield scrapy.Request(url, callback=?)