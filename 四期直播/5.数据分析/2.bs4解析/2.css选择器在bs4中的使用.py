import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://desk.zol.com.cn/pc/"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}

resp = requests.get(url, headers=headers)
resp.encoding = "gbk"

main_page = BeautifulSoup(resp.text, "html.parser")
a_list = main_page.select(".photo-list-padding > a")
for a in a_list:
    href = a.get("href")
    if href.endswith(".exe"):
        continue
    href = urljoin(url, href)
    child_resp = requests.get(href, headers=headers)
    child_resp.encoding = "gbk"
    child_page = BeautifulSoup(child_resp.text, "html.parser")
    src = child_page.select_one("#bigImg").get("src")
    img_resp = requests.get(src, headers=headers)
    fileName = src.split("/")[-1]
    with open(fileName, mode="wb") as f:
        f.write(img_resp.content)
    time.sleep(1)
    child_page.close()
main_page.close()
