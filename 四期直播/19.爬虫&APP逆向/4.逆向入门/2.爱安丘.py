import requests
import random
import string
# import ssl
# print(ssl.OPENSSL_VERSION)


def get_imei():
    return "".join(random.choices(string.digits + 'abcdef', k=16))

imei = get_imei()
session = requests.session()
session.cookies.set("orgid", "137")
session.headers.update({
    "cq-agent":	'{"os":"android","imei":"%s","osversion":"6.0.1","network":"none","version":"0.0.28.108","core":"1.6.4"}' % imei,
    'user-agent': "chuangqi.o.137.com.iqilu.app137/0.0.28.108",
    'orgid': "137"
})

phone_num = input("请输入手机号：")
resp = session.post(
    url="https://app-auth.iqilu.com/member/phonecode",
    json={
        "phone": phone_num
    }
)
resp.close()
res_dict =  resp.json()
print(res_dict)
key = res_dict["data"]
code = input("请输入手机接收到的验证码：")

resp = session.post(
    url="https://app-auth.iqilu.com/member/login",
    json={
        "phone": phone_num,
        "code": code,
        "key": key,
        "password": "",
        "captcha": "",
        "captchaKey": ""
    }
)

print("登录结果：", resp.text)
