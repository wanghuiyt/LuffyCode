# MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDA5Zq6ZdH/RMSvC8WKhp5gj6Ue4Lqjo0Q2PnyGbSkTlYku0HtVzbh3S9F9oHbxeO55E8tEEQ5wj/+52VMLavcuwkDypG66N6c1z0Fo2HgxV3e0tqt1wyNtmbwg7ruIYmFM+dErIpTiLRDvOy+0vgPcBVDfSUHwUSgUtIkyC47UNQIDAQAB
"""
保持住cookie的方案
1.session只能处理response头的cookie
2.js处理的cookie，session是没办法解决的（手工处理）
3.既有响应头，又有js处理
"""
import json
import base64
import requests
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


def base64_api(img):
    data = {"username": "q6035945", "password": "q6035945", "typeid": 3, "image": img}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result["success"]:
        return result["data"]["result"]
    else:
        return result["message"]


session = requests.session()
session.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

# 如何加载第一个cookie
login_page_url = "https://user.wangxiao.cn/login?url=https%3A%2F%2Fks.wangxiao.cn%2F"
session.get(login_page_url)  # 目的：加载第一个cookie
# print(session.cookies)

v_code_url = "https://user.wangxiao.cn/apis//common/getImageCaptcha"
v_code_resp = session.post(v_code_url, headers={"Content-Type": "application/json;charset=UTF-8"})
# print(v_code_resp.json())
img_base64_data = v_code_resp.json()["data"].split(",")[1]
# print(img_base64_data)
# 需要识别图片
with open("tu.png", mode="wb") as f:
    f.write(base64.b64decode(img_base64_data))
# 开始识别
v_code = base64_api(img_base64_data)
# print(v_code)

password = "wangxiao123"

# 先访问getTime
get_time_url = "https://user.wangxiao.cn/apis//common/getTime"
time_resp = session.post(get_time_url, headers={"Content-Type": "application/json;charset=UTF-8"})
time_data = time_resp.json()["data"]

prepare_rsa_enc_str = password + time_data
# 公钥
pub_key_str = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDA5Zq6ZdH/RMSvC8WKhp5gj6Ue4Lqjo0Q2PnyGbSkTlYku0HtVzbh3S9F9oHbxeO55E8tEEQ5wj/+52VMLavcuwkDypG66N6c1z0Fo2HgxV3e0tqt1wyNtmbwg7ruIYmFM+dErIpTiLRDvOy+0vgPcBVDfSUHwUSgUtIkyC47UNQIDAQAB"
pub_key_bytes = base64.b64decode(pub_key_str)
# print(pub_key_bytes)
pub_key = RSA.importKey(pub_key_bytes)
rsa = PKCS1_v1_5.new(pub_key)
psw_bs = rsa.encrypt(prepare_rsa_enc_str.encode("utf_8"))
psw = base64.b64encode(psw_bs).decode()
# print(psw)
login_data = {
    "imageCaptchaCode": v_code,
    "password": psw,
    "userName": "16730231265"
}

login_url = "https://user.wangxiao.cn/apis//login/passwordLogin"
login_resp = session.post(login_url, data=json.dumps(login_data), headers={"Content-Type": "application/json;charset=UTF-8"})
# print(login_resp.json())
login_data = login_resp.json()["data"]

# 完成登录之后需要对Cookie进行设置
session.cookies["autoLogin"] = "true"
session.cookies["userInfo"] = json.dumps(login_data)
session.cookies["token"] = login_data["token"]
session.cookies["UserCookieName"] = login_data["userName"]
session.cookies["OldUsername2"] = login_data["userNameCookies"]
session.cookies["OldUsername"] = login_data["userNameCookies"]
session.cookies["OldPassword"] = login_data["passwordCookies"]
session.cookies["UserCookieName_"] = login_data["userName"]
session.cookies["OldUsername2_"] = login_data["userNameCookies"]
session.cookies["OldUsername_"] = login_data["userNameCookies"]
session.cookies["OldPassword_"] = login_data["passwordCookies"]
tem_key = login_data["userName"] + "_exam"
session.cookies[tem_key] = login_data["sign"]

# print(session.cookies)
test_url = "http://ks.wangxiao.cn/practice/listQuestions"
test_data = {
    "examPointType": "",
    "practiceType": "2",
    "questionType": "",
    "sign": "jz1",
    "subsign": "8cc80ffb9a4a5c114953",
    "top": 30,
}
# 如果能拿到题，登录就没毛病
# 如果拿不到题，反而进入登录页，登录就不成功
resp = session.post(test_url, data=json.dumps(test_data), headers={"Content-Type": "application/json;charset=UTF-8"})
print(resp.text)
