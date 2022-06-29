import requests

# 如果我也能登录，那么我应该也能获取到set-cookie
# 走一遍登录流程，应该就能拿到cookie

# 用户名 密码 url
# 16538989670 q6035945

url = "https://passport.17k.com/ck/user/login"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}

data = {
    "loginName": "16538989670",
    "password": "q6035945"
}

resp = requests.post(url, data=data, headers=headers)
# print(resp.json())
# print(resp.headers)
# 如何拿到这一堆cookie
# print(resp.headers["Set-Cookie"])  # 字符串
# print(resp.cookies)  # requests-cookie的样子
d = resp.cookies  # requestscookieJar

# 查看书架
url = "https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919"
resp_2 = requests.get(url, cookies=d)
print(resp_2.text)

# 可以自动的保持会话(自动处理cookie)
session = requests.session()
