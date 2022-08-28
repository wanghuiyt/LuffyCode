import requests
import execjs
import os

with open("sdk2.js", mode='r', encoding="utf-8") as f:
    js = f.read()

JS = execjs.compile(js)

url = "https://www.toutiao.com/api/pc/list/feed?channel_id=3189398972&max_behot_time=1661647455&category=pc_profile_channel&client_extra_params=%7B%22short_video_item%22:%22filter%22%7D&aid=24&app_name=toutiao_web"
signature = JS.call("get_sign", url)
print(signature)
final_url = f"{url}&_signature={signature}"
resp = requests.get(
    url=final_url,
    headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }
)
print(resp.text)
