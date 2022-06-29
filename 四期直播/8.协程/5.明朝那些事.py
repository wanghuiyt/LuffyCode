import os
import asyncio
import aiohttp
import aiofiles
import requests
from lxml import etree


# 1.拿到主页面的源代码(不需要异步)
# 2.拿到页面源代码之后，需要解析出<卷名>，<章节, href>
# 3.xxx

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "cookie": "_ga=GA1.2.1847446236.1656240732; _gid=GA1.2.1931311355.1656240732; __gads=ID=d5ad5450601b2252-22b0753fccd400c7:T=1656240732:RT=1656240732:S=ALNI_MaW1A6hyf3RYgAvpY41ybnnYv0cjA; __gpi=UID=000006fa798349c3:T=1656240732:RT=1656240732:S=ALNI_MZV4IDkRY2E6u-HKCWz_FFwccIzvQ",
}


def get_chapter_info(url):
    resp = requests.get(url, headers=headers, verify=False)
    resp.encoding = "utf-8"
    page_source = resp.text
    print(page_source)
    # 开始解析
    root = etree.HTML(page_source)  # type: etree._Element
    """
    [{"juan_ming":"万国来朝","chapter":[{"chapter_name":"第一章","chapter_url":href},{},{}]},
     {},
     {}]
     [
        {"juan_name":"万国来朝","chapter_name":"第一章","chapter_url":href},
        {"juan_name":"万国来朝","chapter_name":"第一章","chapter_url":href},
        {"juan_name":"万国来朝","chapter_name":"第一章","chapter_url":href},
        ...
        {"juan_name":"万国来朝","chapter_name":"第一章","chapter_url":href}
     ]
    """

    result = []
    divs = root.xpath("//div[@class='mulu']")  # 每一个div就是一卷
    for div in divs:
        trs = div.xpath(".//table/tr")  # 一堆tr
        juan_name = trs[0].xpath(".//a/text()")
        juan_name = "".join(juan_name).strip().replace("：", "_")
        for tr in trs[1:]:
            # texts = tr.xpath("./td//text()")
            # urls = tr.xpath("./td/a/@href")
            # print(texts, urls)
            tds = tr.xpath("./td")
            for td in tds:
                txt = td.xpath(".//text()")
                href = td.xpath(".//@href")
                txt = "".join(txt).replace(" ", "").strip()
                href = "".join(href)
                if txt == "\xa0" or href == "":
                    continue
                dic = {
                    "juan_name": juan_name,
                    "chapter_name": txt,
                    "chapter_url": href
                }
                result.append(dic)
    return result


async def download_one(url, file_path):
    print("开始下载文章了")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            page_source = await resp.text(encoding="utf-8")
            # print(page_source)
            root = etree.HTML(page_source)  # type: etree._Element
            content = root.xpath("//div[@class='content']//p//text()")
            content = "".join(content).replace("\n", "").replace("\r", "").replace(" ", "").strip()
            async with aiofiles.open(file_path, mode="w", encoding="utf-8") as f:
                await f.write(content)
    print(f"{file_path}下载完成")


async def download_chapter(chapter_list):
    tasks = []
    for chapter in chapter_list:
        juan_name = chapter["juan_name"]
        name = chapter["chapter_name"]
        url = chapter["chapter_url"]
        if not os.path.exists(juan_name):
            os.makedirs(juan_name)
        # 给出文件的真正的保存路径
        file_path = f"{juan_name}/{name}.txt"
        print(file_path)
        t = asyncio.create_task(download_one(url, file_path))
        tasks.append(t)
        # break  # 测试的时候
    await asyncio.wait(tasks)


def main():
    url = "https://www.mingchaonaxieshier.com/"
    chapter_list = get_chapter_info(url)
    # print(chapter_list)
    # 开始上协程，进行异步下载
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(download_chapter(chapter_list))


if __name__ == '__main__':
    main()
