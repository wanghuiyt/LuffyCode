import scrapy
from scrapy.http.response.html import HtmlResponse


class DengSpider(scrapy.Spider):
    name = 'deng'
    allowed_domains = ['17k.com']
    start_urls = ['https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919']
    # 能不能找到第一次请求，并把cookie直接给它塞进去

    # 在符类中找到了一个start_requests的函数，这个函数中，循环了start_urls,并将每一个url封装成了一个请求对象Request
    def start_requests(self):
        s = 'GUID=ca5f2a6a-de90-4e83-8c99-5ee8a83fa011; accessToken=avatarUrl%3Dhttps%253A%252F%252Fcdn.static.17k.com%252Fuser%252Favatar%252F19%252F99%252F14%252F95041499.jpg-88x88%253Fv%253D1648893235000%26id%3D95041499%26nickname%3D%25E5%2598%25BB%25E5%2598%25BB%25E5%2598%25BB%25E7%259A%2584%25E6%259D%25B0%25E4%25BC%25A6%26e%3D1674118107%26s%3D4ae115760935c661; c_channel=0; c_csc=web; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2295041499%22%2C%22%24device_id%22%3A%221819959e2bb9ad-0492a9a56fcba6-26021b51-3110400-1819959e2bcd2a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22ca5f2a6a-de90-4e83-8c99-5ee8a83fa011%22%7D; Hm_lvt_9793f42b498361373512340937deb2a0=1658563449,1659477926; Hm_lpvt_9793f42b498361373512340937deb2a0=1659478480'
        dic = {}
        for item in s.split("; "):
            k, v = item.split("=")
            dic[k] = v

        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True, cookies=dic)


    def parse(self, resp: HtmlResponse, **kwargs):
        print(resp.text)
