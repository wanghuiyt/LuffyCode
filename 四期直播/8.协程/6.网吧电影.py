import re
import requests
import asyncio
import aiohttp
import aiofiles
from lxml import etree
from urllib.parse import urljoin


"""
整体步骤
1.想办法找到M3U8文件
2.判别是否需要下载第二层M3U8
3.提取ts文件的下载路径
4.下载
5.判别是否需要解密
6.如果需要解密，拿到密钥
7.解密
8.根据M3U8正确顺序来合并所有的ts文件==>MP4
"""
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
}


def get_iframe_src(url):
    resp = requests.get(url, headers=headers)
    root = etree.HTML(resp.text)  # type: etree._Element
    src = root.xpath("//iframe/@src")[0]
    return src


def get_m3u8_url(url):
    resp = requests.get(url, headers=headers)
    print(resp.text)
    obj = re.compile(r'url: "(?P<m3u8>.*?)"')
    m3u8 = obj.search(resp.text).group("m3u8")
    return m3u8


def download_m3u8(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers)
    with open("first.m3u8", mode="w", encoding="utf-8") as f:
        f.write(resp.text)
    with open("first.m3u8", mode="r", encoding="utf-8") as f2:
        for line in f2:
            if line.startswith("#"):
                continue
            # 此时的line就是第二层M3U8的地址
            line = line.strip()  # 有换行存在，要去掉
            line = urljoin(url, line)
            resp = requests.get(line, headers=headers)
            with open("second.m3u8", mode="w", encoding="utf-8") as f3:
                f3.write(resp.text)
                break


async def download_all_videos():
    # 1.读取文件
    with open("second.m3u8", mode="r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            line = line.strip()  # 这里一定要加上，每次都要强调
            # 此时，line就是下载地址
    # 2.创建任务

    # 3.统一等待
    pass


def main():
    url = "http://www.wbdy.tv/play/63690_1_1.html"
    # 1.拿到iframe的src属性值
    src = get_iframe_src(url)
    # print(src)
    # 2.发送请求到iframe的src路径，获取M3U8地址
    src = urljoin(url, src)
    m3u8_url = get_m3u8_url(src)
    # print(m3u8_url)
    # 3.下载m3u8文件
    download_m3u8(m3u8_url)
    # 4.下载视频.上协程下载视频
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(download_all_videos)


if __name__ == '__main__':
    main()
