import requests
import pymongo
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}


def get_page_source(url):
    resp = requests.get(url, headers=headers)
    return resp.text


def parse_data(pgSource):
    tree = etree.HTML(pgSource)  # type: etree._Element
    li_list = tree.xpath('//*[@class="sellListContent"]/li')
    # print(len(li_list))
    result = []
    for li in li_list:
        title = li.xpath('.//*[@class="title"]/a/text()')
        if not title:
            continue
        title = title[0]  # 根据你的实际情况，取[0]或者用join()处理
        position = li.xpath('.//*[@class="positionInfo"]//text()')
        position = "".join([item.strip() for item in position])
        house_infos = li.xpath('.//*[@class="houseInfo"]//text()')
        infos = house_infos[0].replace(" ","").split("|")
        total = li.xpath('.//*[@class="priceInfo"]/div[1]//text()')
        total = "".join(total)
        price = li.xpath('.//*[@class="priceInfo"]/div[2]//text()')
        price = price[0].replace(",", "")
        dic = {
            "title": title,
            "position": position,
            "infos": infos,
            "total": total,
            "price": price
        }
        result.append(dic)
    return result


def save_data(data):
    conn = pymongo.MongoClient(host="localhost", port=27017)
    db = conn["cool"]
    db.yunsir.insert_many(data)


def main():
    url = "https://bj.lianjia.com/ershoufang/"
    page_source = get_page_source(url)
    data = parse_data(page_source)
    save_data(data)

if __name__ == '__main__':
    main()
