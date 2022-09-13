import re
import copy
import time
import json
import string
import random
import base64
import requests
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Util.Padding import pad
from urllib.parse import quote_plus, urlsplit, quote
from hashlib import md5, sha256, sha1


class Bilibili(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.region, self.mobile, self.card_url = None, None, None

        self.build_brand = None
        self.build_model = None
        self.wifi_mac = None
        self.device_id = None
        self.buvid = None
        self.android_id = None
        self.session_id = None
        self.build_fingerprint = None
        self.build_display = None

        self.fp_local = None
        self.fp_remote = None
        self.app_first_run_time = None
        self.ts = str(int(time.time() - 10))

        self.hash = None
        self.rsa_pub_key = None
        self.guest_id = None
        self.captcha_key = None
        self.is_new = None
        self.cookie_info = None
        self.token_info = None
        self.proxy_dict = None

        self.initialize()

        self.session = requests.session()
        self.session.proxies = self.get_proxy_dict()

    def initialize(self):
        with open(self.file_path, mode="r", encoding="utf-8") as f:
            data_dict = json.load(f)
        for k, v in data_dict.items():
            setattr(self, k, v)

    @staticmethod
    def get_proxy_dict():
        # key = "tps150.kdlapi.com:15818"
        # passwd = "t12678079599196"
        # host = "gbtn0lkl"
        # return {
        #     "http": 'http://{}:{}@{}'.format(key, passwd, host),
        #     "https": 'https://{}:{}@{}'.format(key, passwd, host)
        # }

        key = "9CEF198A"  # 用户key
        passwd = "3FD919941B70"  # 用户密码

        resp = requests.get(
            url="https://proxy.qg.net/extract?Key=9CEF198A&Num=1&AreaId=&Isp=&DataFormat=txt&DataSeparator=%5Cr%5Cn&Detail=0"
        )

        # host = resp.json()['Data'][0]['host']  # 121.29.81.215:52001
        host = resp.text
        print(host)

        # 账密模式
        proxy = 'http://{}:{}@{}'.format(key, passwd, host)
        return {"http": proxy, "https": proxy}

    @staticmethod
    def md5_encrypt(data_string, isBytes=False):
        obj = md5()
        obj.update(data_string.encode("utf-8"))
        if isBytes:
            return obj.digest()
        return obj.hexdigest()

    @staticmethod
    def sha256_encrypt(data_string):
        SALT = "9cafa6466a028bfb"
        sha = sha256()
        sha.update(data_string.encode("utf-8"))
        sha.update(SALT.encode("utf-8"))
        return sha.hexdigest()

    @staticmethod
    def sha1_encrypt(data_string):
        obj = sha1()
        obj.update(data_string.encode("utf-8"))
        return obj.hexdigest()

    @staticmethod
    def aes_encrypt(data_string, key, iv):
        aes = AES.new(
            key=key.encode("utf-8"),
            mode=AES.MODE_CBC,
            iv=iv.encode("utf-8")
        )
        raw = pad(data_string.encode("utf-8"), 16)
        encrypt_bytes = aes.encrypt(raw)
        hex_string = "".join(["%02x" % b for b in encrypt_bytes])
        return hex_string

    @staticmethod
    def base64_encrypt(data_string):
        data_bytes = bytearray(data_string.encode('utf-8'))
        data_bytes[0] = data_bytes[0] ^ (len(data_bytes) & 0xFF)
        for i in range(1, len(data_bytes)):
            data_bytes[i] = (data_bytes[i - 1] ^ data_bytes[i]) & 0xFF
        res = base64.encodebytes(bytes(data_bytes))
        return res.strip().strip(b"==").decode('utf-8')

    def rsa_encrypt(self, data_string):
        """
        使用RSA公钥加密
        :param data_string:
        :return:
        """
        key = RSA.importKey(self.rsa_pub_key)
        cipher = PKCS1_v1_5.new(key)
        ciphertext = base64.b64encode(cipher.encrypt(bytes(data_string, "utf-8")))
        return ciphertext

    def get_param_sign_s(self, param_dict):
        """
        根据param_dict中的key排序，拼接，md5计算，拼接sign，并返回
        :param param_dict: 要签名的参数字典
        :return:
        """
        ordered_string = "&".join([f"{key}={param_dict[key]}" for key in sorted(param_dict.keys())])
        data_string = ordered_string + "560c52ccd288fed045859ed18bffd973"
        obj = md5(data_string.encode("utf-8"))
        sign = obj.hexdigest()

        return f"{ordered_string}&sign={sign}"

    def get_param_sign_so(self, param_dict):
        """
        根据param_dict中的key排序，拼接，md5计算，拼接sign，并返回
        :param param_dict: 要签名的参数字典
        :return:
        """
        ordered_string = "&".join([f"{key}={param_dict[key]}" for key in sorted(param_dict.keys())])
        data_string = ordered_string + "60698ba2f68e01ce44738920a0ffe768"
        obj = md5(data_string.encode("utf-8"))
        sign = obj.hexdigest()

        return f"{ordered_string}&sign={sign}"

    def status(self):
        data_dict = {
            "access_key": self.token_info["access_token"],
            "appkey": "1d8b6e7d45233436",
            "build": "6240300",
            "channel": "xxl_gdt_wm_253",
            "mobi_app": "android",
            "platform": "android",
            "re_src": "0",
            "statistics": quote_plus(json.dumps({"appId": 1, "platform": 3, "version": "6.24.0", "abtest": ""}, separators=(",", ":"))),
            "ts": int(time.time()),
        }


def run():
    file_path = "5813346972.txt"

    bili = Bilibili(file_path)

    while True:
        time.sleep(1)
        info_dict = bili.status()


if __name__ == '__main__':
    run()
    # print(int(time.time()))
