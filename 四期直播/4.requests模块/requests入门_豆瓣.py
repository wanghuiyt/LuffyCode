# 方法论
# 任何一个网站，第一件事，观察你要的东西在不在页面源代码
# 如果在，直接请求url即可
# 如果不在，抓包工具观察，数据究竟在哪个url加载进来的
import requests

# 方案一，参数太长，看起来费劲
# url = "https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=0&limit=20"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
# }
# resp = requests.get(url, headers=headers)
# # print(resp.text)
# print(resp.json())

# 方案二
url = "https://movie.douban.com/j/chart/top_list"
dic = {
    "type": "13",
    "interval_id": "100:90",
    "action": "",
    "start": "0",
    "limit": "20"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
}
# 发送get请求，并将参数带进去
# resp = requests.get(url, params=dic, headers=headers)
# print(resp.json())
# print(resp.request.url)

# for i in range([0, 20, 40, 60, 80]):
# for i in range(0, 100, 20):
for i in range(5):
    dic["start"] = str(i*20)
    resp = requests.get(url, params=dic, headers=headers)
    # print(resp.json())
    content = resp.json()
    for item in content:
        print(f"{item['title']}|{item['score']}|{item['cover_url']}")

