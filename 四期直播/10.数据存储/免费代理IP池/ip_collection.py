"""
负责代理IP的采集工作
"""
import time
import requests
from lxml import etree
from proxy_redis import ProxyRedis
from multiprocessing import Process

r = ProxyRedis()
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}


def get_ip(url):
    resp = requests.get(url, headers=headers)
    tree = etree.HTML(resp.text)  # type: etree._Element
    trs = tree.xpath('//table/tbody/tr')
    for tr in trs:
        ip = tr.xpath("./td[1]/text()")  # ip
        port = tr.xpath("./td[2]/text()")  # port
        # print(ip, port)
        if not ip:
            continue
        ip = ip[0]
        port = port[0]
        proxy_ip = f"{ip}:{port}"
        r.add_proxy_ip(proxy_ip)  # 增加新的IP地址


def run():
    while True:
        try:
            get_ip("https://free.kuaidaili.com/free/intr/")
            get_ip("https://ip.jiangxianli.com/?page=1")
        except Exception as ex:
            print("获取IP崩溃了", ex.args)
        time.sleep(60)


if __name__ == '__main__':
    # r = ProxyRedis()
    # get_kuai_ip(r)
    # get_jxl_ip(r)
    p = Process(target=run)
    p.start()
