# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from scrapy.http.response.html import HtmlResponse
from zhipin.req import SeleniumRequest

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class ZhipinSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ZhipinDownloaderMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_request(self, request, spider):
        if isinstance(request, SeleniumRequest):
            # 使用selenium来完成页面源代码（elements）的抓取
            self.web.get(request.url)  # 直接访问即可
            self.web.find_element(By.XPATH, '//*[@id="header"]/div[1]/div[3]/div/a[1]')  # 随便找个东西，如果找到了，就算加载完了
            page_source = self.web.page_source  # 就可以拿页面源代码了
            # 页面源代码有了，下载器还去吗？--不去
            # 组装一个响应对象，返回 -> 引擎
            resp = HtmlResponse(
                status=200,
                url=request.url,
                body=page_source.encode("utf-8"),
                request=request
            )
            return resp
        else:
            return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
        options = ChromeOptions()
        # options.add_argument("--headless")  # 无头
        options.binary_location = r"D:\SoftWare\Google\Chrome\Application\chrome.exe"
        self.web = Chrome(options=options)  # 程序跑起来之后，去创建Chrome对象。程序跑完之后，关掉web对象
        self.web.implicitly_wait(10)  # 等待

    def spider_closed(self, spider):
        self.web.close()
