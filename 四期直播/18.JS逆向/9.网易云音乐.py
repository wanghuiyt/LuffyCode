import binascii
import json
import base64
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def b(data, key):
    key = key.encode("utf-8")
    data = data.encode("utf-8")
    data = pad(data, 16)
    aes = AES.new(key=key, IV=b"0102030405060708", mode=AES.MODE_CBC)
    bs = aes.encrypt(data)
    return base64.b64encode(bs).decode()


# 暂时不管这个rsa加密
def c(i, e, f):
    i = i[::-1]  # 从后往前加密
    e = int(e, 16)
    f = int(f, 16)
    bs = i.encode("utf-8")
    s = binascii.b2a_hex(bs).decode()
    s = int(s, 16)
    # 全是数字
    mi = (s**e) % f
    return format(mi, "x")  # 转成十六进制数
    # return "d6cf71ac77cd9f94cc877657b5cee28488e4efc26ca5a22c2b8cc01b6ec9ad0fe8dc65e510ad40386551e2db64660de8c21ccd0bba08304f24bf5fd92336c2fe6492f0e7f043c23a9050c4caedef490ecf48491557bfe438947d939531ee91218b04ea1593424da35daccbf39667a62f65766ff9272f81d89d7bf684cf083643"

def asrsea(data, e, f, g):
    i = "Y5oLbwFDuYI9MCws"
    first = b(data, g)
    encText = b(first, i)
    # 对i进行rsa加密
    encSecKey = c(i, e, f)
    return  encText, encSecKey


def main():
    # 数据加密前的样子
    url = "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token="
    data = {
        "encodeType": "aac",
        "ids": [1325905146],
        "level": "standard",
        "csrf_token": ""
    }
    data = json.dumps(data)
    e = "010001"
    f = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    g = "0CoJUm6Qyw8W8jud"
    encText, encSecKey = asrsea(data, e, f, g)

    dic = {
        "params": encText,
        "encSecKey": encSecKey
    }

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }

    resp = requests.post(url, data=dic, headers=headers)
    resp_dict = resp.json()
    sounds = resp_dict["data"]
    for sound in sounds:
        sound_url = sound["url"]
        sound_id = sound["id"]
        sound_resp = requests.get(sound_url)
        with open(f"{sound_id}.m4a", mode="wb") as f:
            f.write(sound_resp.content)

if __name__ == '__main__':
    main()

