# 用requests来完成登录过程
# 一般情况下，在使用验证码的时候，要保持住会话，否则容易引起，验证码识别不成功的现象
import requests
import json


def base64_api(uname, pwd, img, typeid):
    data = {
        "username": uname,
        "password": pwd,
        "typeid": typeid,
        "image": img
    }
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result["success"]:
        return result["data"]["result"]
    else:
        return result["message"]


session = requests.session()
# 1.设置好头信息
session.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}
# 2.加载一个最原始的cookie（可能需要可能不需要，好习惯）
session.get("http://www.ttshitu.com/login.html?spm=null")
# 3.发送请求，拿到验证码
verify_url = "http://admin.ttshitu.com/captcha_v2?_=1658152264206"  # url屁股上总能看见_ t n => 时间戳，防止浏览器缓存
resp = session.get(verify_url)
img = resp.json()["img"]  # 拿图片
imgId = resp.json()["imgId"]  # 图片ID
# print(img)
# print(imgId)
username = "q6035945"
password = "q6035945"
# 4.识别验证码
verify_code = base64_api(username, password, img, 1)
# 准备登录
login_url = "http://admin.ttshitu.com/common/api/login/user"
data = {"userName": username, "password": password, "captcha": verify_code, "imgId": imgId, "developerFlag": False, "needCheck": True}
# 我们在浏览器中发现了一种全新的参数逻辑
# queryString  url
# form data  post(data=data)
# Request Payload
# 1.发送出去的是json
# 2.请求一定是post
# 3.它的请求头里一定又content-ype: application/json
# resp = session.post(login_url, data=json.dumps(data), headers={"Content-Type": "application/json; charset=UTF-8"})
resp = session.post(login_url, json=data)  # 如果给了json参数，自动的帮你转化和处理，以及请求头的处理
print(resp.text)
