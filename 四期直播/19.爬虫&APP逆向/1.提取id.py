import re
import math
import json
import random
import time

import requests

url = "https://www.bilibili.com/video/BV1N94y1R7K5"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

resp = requests.get(url, headers=headers)
print(resp.cookies.get_dict())
data = re.search(r'__INITIAL_STATE__=(?P<page>.+);\(function', resp.text).group("page")
data_dict = json.loads(data)
aid = data_dict["aid"]
cid = data_dict["videoData"]["cid"]
print(aid)
print(cid)

data = ""
for i in range(8):
    v1 = math.ceil(16 * random.uniform(0, 1))
    v2 = hex(v1)[2:].upper()
    data += v2
result = data.rjust(8, "0")

e = int(time.time() * 1000)
t = hex(e)[2:].upper()

b_lsid = f"{result}_{t}"
print(b_lsid)
