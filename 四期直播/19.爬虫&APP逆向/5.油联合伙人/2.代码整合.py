import time
import requests
from hashlib import md5


def myMd5(data_string):
    obj = md5()
    obj.update(data_string.encode("utf-8"))
    return obj.hexdigest()


def run():
    phone = input("请输入手机号：")
    password = input("请输入密码：")
    encrypt_pwd = myMd5(password)

    token = ""
    reqTime = str(int(time.time() * 1000))
    nonce_str = "123456"
    nonce_str_sub_2 = nonce_str[2:]
    body_str = f"phone={phone}&password={encrypt_pwd}"
    encrypt_str = f"{token}{reqTime}{nonce_str_sub_2}{body_str}"

    sign = myMd5(encrypt_str)

    resp = requests.post(
        url="https://chinayltx.com/app/api/v1/partnerLogin/login",
        data={
            "phone": phone,
            "password": encrypt_pwd
        },
        headers={
            "X-App": "native",
            "X-Noncestr": nonce_str,
            "X-OS": "partnerApp_android",
            "X-Req-Time": reqTime,
            "X-Sign": sign,
            "X-Token": token,
            "X-UserID": ""
        }
    )

    print(resp.text)


if __name__ == '__main__':
    run()
