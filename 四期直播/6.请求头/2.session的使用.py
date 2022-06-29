import requests

# 1.创建一个session
# session 会自动处理和更新requests headers 中的set-cookie
# 但是javascript中的set-cookie无法处理
# session = requests.session()

with requests.session() as session:
    # 2.可以提前给session设置好请求头或者cookie
    session.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }

    # 可用可不用
    # session.cookies = {
    #     # 可以把一些cookie的内容塞进来，这里要的是字典
    # }

    # 3.发请求
    url = "https://passport.17k.com/ck/user/login"
    data = {
        "loginName": "16538989670",
        "password": "q6035945"
    }
    # 在这一次请求中，把User-Agent临时更换成你给的这个，但是不影响原来的session
    session.post(url, data=data, headers={"User-Agent": "xxx"})
    # print(session.cookies)

    url = "https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919"
    resp = session.get(url)
    print(resp.text)


