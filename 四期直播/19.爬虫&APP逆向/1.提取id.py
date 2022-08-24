import re
import json
import requests

url = "https://www.bilibili.com/video/BV1N94y1R7K5"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

resp = requests.get(url, headers=headers)
data = re.search(r'__INITIAL_STATE__=(?P<page>.+);\(function', resp.text).group("page")
data_dict = json.loads(data)
aid = data_dict["aid"]
cid = data_dict["videoData"]["cid"]
print(aid)
print(cid)

