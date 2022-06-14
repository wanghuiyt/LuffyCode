import json

import requests
import json

# GET
# url = "https://www.sogou.com/web?query=周杰伦"
# # resp = requests.get(url)
# # print(resp)
# # print(resp.text)
# # 响应.请求.请求头(UA)
# # print(resp.request.headers)
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
# }
#
# resp = requests.get(url, headers=headers)
# print(resp.text)

# POST
url = "https://fanyi.baidu.com/sug"
data = {
    "kw": "jay"
}
resp = requests.post(url, data=data)
print(resp.text)  # 确认一下是否是json，单纯拿文本、html、json => 字符串
# print(json.loads(resp.text))  # 方案1
print(resp.json())  # 方案2，前提是服务器返货的必须是json字符串，只能拿json => 字典


