import time
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor


def str_tools(lst):
    if lst:
        return "".join(lst).strip()
    else:
        return ""


def get_movie_info(year):
    url = f"http://www.boxofficecn.com/boxoffice{year}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers)
    main_page = etree.HTML(resp.text)  # type: etree._Element
    tr_list = main_page.xpath("//table/tbody/tr")[1:]
    with open(f"{year}.csv", mode="w", encoding="utf-8") as f:
        for tr in tr_list:
            num = str_tools(tr.xpath("./td[1]//text()"))
            year = str_tools(tr.xpath("./td[2]//text()"))
            name = str_tools(tr.xpath("./td[3]//text()"))
            money = str_tools(tr.xpath("./td[4]//text()"))
            # print(num, year, name, money)
            f.write(f"{num},{year},{name},{money}\n")


if __name__ == '__main__':
    # s1 = time.time()  # 当前系统的时间戳
    # for i in range(1994, 2023):
    #     get_movie_info(i)
    # s2 = time.time()  # 执行之后的时间戳
    # print(s2 - s1)  # 15.38
    s1 = time.time()  # 当前系统的时间戳
    with ThreadPoolExecutor(16) as t:
        for i in range(1994, 2023):
            t.submit(get_movie_info, i)
    s2 = time.time()  # 执行之后的时间戳
    print(s2 - s1)  # 12.21
