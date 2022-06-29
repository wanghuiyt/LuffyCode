import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}

dic = {
    "http": "http://223.96.90.216:8085",
    "https": "https://223.96.90.216:8085",
}

resp = requests.get("https://www.baidu.com/s?wd=ip&ie=UTF-8", headers=headers, proxies=dic)
print(resp.text)
