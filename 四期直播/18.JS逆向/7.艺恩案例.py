"""
https://www.endata.com.cn/BoxOffice/BO/Year/index.html
ob混淆：
    完全手撸（上课选择）
    抠代码（补环境->jsdom）
    AST（入门难度极高）
"""

# 把16进制字符串变成字节，把字节变成16进制字符串
import json
import requests
import binascii
from Crypto.Cipher import DES

def func(a, b, c):
    if b == 0:
        return a[c:]
    r = a[:b]
    d = b + c
    r += a[d:]
    return r

def shell(data):
    a = int(data[-1], 16) + 9
    b = int(data[a], 16)
    data = func(data, a, 1)
    a = data[b: b + 8]
    data = func(data, b, 8)

    # 16进制的字符串，需要还原成字节
    print(data)
    if data[-1] == "0":
        data = data[:-1]
    bs = binascii.a2b_hex(data)
    # bs = bytes.fromhex(data)
    # 开始DESC解密
    key = a.encode("utf-8")
    s = DES_DECRYPT(bs, key).decode("utf-8")
    s = s[:s.rindex("}")+1]  # 取到最后一个大括号的位置
    dic = json.loads(s)
    return dic


def DES_DECRYPT(data, key):
    des = DES.new(key=key, mode=DES.MODE_ECB)
    bs = des.decrypt(data)
    return bs


if __name__ == '__main__':
    url = "https://www.endata.com.cn/API/GetData.ashx"
    data = {
        'year': 2022,
        'MethodName': 'BoxOffice_GetYearInfoData'
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    resp = requests.post(url, data=data, headers=headers)
    dic = shell(resp.text)
    print(dic)
