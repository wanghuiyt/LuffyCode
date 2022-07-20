import time
from lxml import etree
from selenium.webdriver import Chrome, ChromeOptions

options = ChromeOptions()
options.binary_location = r"D:\SoftWare\Google\Chrome\Application\chrome.exe"
web = Chrome(options=options)
web.implicitly_wait(10)


def get_page_source(url):
    web.get(url)
    time.sleep(3)
    return web.page_source  # selenium 中的page_source是elements


if __name__ == '__main__':
    url = "https://search.bilibili.com/all?keyword=%E5%87%A4%E5%87%B0%E8%8A%B1%E5%BC%80%E7%9A%84%E8%B7%AF%E5%8F%A3&from_source=webtop_search&spm_id_from=333.1007"
    page_source = get_page_source(url)
    tree = etree.HTML(page_source)  # type: etree._Element
    txt = tree.xpath('//*[@class="bili-video-card"]//h3/@title')
    print(txt)