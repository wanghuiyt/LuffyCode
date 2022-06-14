"""
https://movie.douban.com/typerank?type_name=%E7%88%B1%E6%83%85&type=13&interval_id=100:90&action=
爬取前100个电影的 名称 分数 封面图url
"""
import json
from urllib.request import Request, urlopen

req = Request("https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=0&limit=100",
              headers={
                  "Referer": "https://movie.douban.com/typerank?type_name=%E7%88%B1%E6%83%85&type=13&interval_id=100:90&action=",
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1;WOW64) AppleWebKit/537.36 (KHTML,like GeCKO) Chrome/45.0.2454.85 Safari/537.36 115Broswer/6.0.3',
                  'Connection': 'keep-alive'
              })
resp = urlopen(req)
res = resp.read()
dic = json.loads(res.decode("utf-8"))
for item in dic:
    print(f'{item["title"]}|{item["score"]}|{item["cover_url"]}')


# url = "http://www.baidu.com"
# resp = urlopen(url)
# # print(resp)
# # 从响应对象中，提取到你需要的东西
# result = resp.read()
# # print(result)
# print(result.decode("utf-8"))
#
# with open("baidu.html", mode="w", encoding="utf-8") as f:
#     f.write(result.decode("utf-8"))

