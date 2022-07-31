import requests

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}


def get_proxy():
    url = "http://127.0.0.1:5804/get_proxy"
    resp = requests.get(url, headers=headers)
    dic = resp.json()
    print(dic)
    proxy = {
        "http": f"http://{dic['ip']}",
        "https": f"http://{dic['ip']}"
    }
    print(proxy)
    return proxy

url = "http://www.baidu.com/s?wd=ip"
"""
上述url会自动的重定向到https上 
requests会自动的像浏览器一样帮助我们完成这个重定向
第一次请求的是http，被重定向了
第二次请求的是https
"""
resp = requests.get(url, proxies=get_proxy(), headers=headers)
print(resp.text)
