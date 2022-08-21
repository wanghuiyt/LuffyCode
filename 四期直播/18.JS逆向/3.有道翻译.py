import random
import time
import execjs
import requests
from 各种加密算法.mymd5 import md5_sign


url = "https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"

headers = {
    "Referer": "https://fanyi.youdao.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    'Cookie': '_ga=GA1.2.796178035.1649565485; OUTFOX_SEARCH_USER_ID_NCOO=1536096603.5078137; OUTFOX_SEARCH_USER_ID="23485477@10.105.137.204"; ___rl__test__cookies=1661060732107'
}

word = input("请输入一个单词：")

# with open("ydfy.js", mode="r", encoding="utf-8") as f:
#     js = f.read()
# obj = execjs.compile(js)
# r = obj.call("fn", word)
# print(type(r))
# r["salt"]  r["sign"]   r["ts"]  r["sign"]

appVarsion = "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
bv = md5_sign(appVarsion)
lts = int(time.time() * 1000)
i = random.randint(0, 10)
salt = int(f"{lts}{i}")
sign = md5_sign(f"fanyideskweb{word}{salt}Ygy_4c=r#e#4EX^NUGUc5")

data = {
"i": word,
"from": "en",
"to": "zh-CHS",
"smartresult": "dict",
"client": "fanyideskweb",
"salt": salt,
"sign": sign,
"lts": lts,
"bv": bv,
"doctype": "json",
"version": "2.1",
"keyfrom": "fanyi.web",
"action": "FY_BY_REALTlME"
}
# print(data)
resp = requests.post(url, headers=headers, data=data)
print(resp.json())

