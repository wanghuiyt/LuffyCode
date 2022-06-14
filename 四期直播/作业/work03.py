"""
爬取动画影评网首页，练习正则
"""
import re
import time
import requests

url = "https://www.animationcritics.com/chinese_aniamtion.html"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36"
}
resp = requests.get(url, headers=headers)
main_page_source = resp.text
main_obj = re.compile(r'<li style="margin-bottom:10px;">.*?href="(?P<url>.*?)" "title="(?P<title>.*?)"', re.S)
laiyuan_obj = re.compile(r'来源:<span>(?P<laiyuan>.*?)</span>', re.S)
zuozhe_obj = re.compile(r'作者:<span>(?P<zuozhe>.*?)</span>', re.S)
section_obj = re.compile(r'<section.*?>(?P<content>.*?)</section>', re.S)
p_obj = re.compile(r'<p data-track.*?>(?P<content>.*?)</p>', re.S)
content_obj = re.compile(r'<.*?>', re.S)

# re.S 让.能匹配换行

# 匹配东西
result = main_obj.finditer(main_page_source, re.S)
for item in result:
    child_url = item.group("url")
    child_title = item.group("title")
    # print(child_url, child_title)
    # 访问详情页
    child_resp = requests.get(child_url, headers=headers)
    child_page_source = child_resp.text
    # print(child_page_source)
    # 对详情页进行数据提取
    lyr = laiyuan_obj.search(child_page_source, re.S)
    if lyr:
        laiyuan = lyr.group("laiyuan")
        # print(laiyuan)
    else:
        laiyuan = ""

    zzr = zuozhe_obj.search(child_page_source, re.S)
    if zzr:
        zuozhe = zzr.group("zuozhe")
    else:
        zuozhe = ""
    # 内容怎么搞？
    # 拿所有section中的内容
    sec_list = []
    section_results = section_obj.finditer(child_page_source, re.S)
    if not section_results:
        section_results = p_obj.finditer(child_page_source, re.S)
    for section in section_results:
        content = section.group("content")
        sec_list.append(content)
    all_content = "".join(sec_list)
    print(all_content)

    # 用正则表达式替换内容 re.sub()
    # 结果 = re.sub(正则， 替换之后的结果， 整个字符串)
    # result = re.sub(r'<.*?>', "", all_content)
    result = content_obj.sub("", all_content)
    print(result)
    time.sleep(1)


























