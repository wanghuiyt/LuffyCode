from lxml import etree
import requests

# 1.拿页面源代码
url = "http://www.boxofficecn.com/boxoffice2019"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}
source_page = requests.get(url, headers=headers).text
# print(source_page.text)
# 2.xpath提取数据
page = etree.HTML(source_page)  # type: etree._Element
tr_list = page.xpath("//table/tbody/tr")[1:-1]
for tr in tr_list:
    num = tr.xpath("./td[1]/text()")
    year = tr.xpath("./td[2]//text()")
    name = tr.xpath("./td[3]//text()")
    if name:
        name = "".join(name)
    else:
        name = ""
    money = tr.xpath("./td[4]/text()")
    print(num, year, name, money)




