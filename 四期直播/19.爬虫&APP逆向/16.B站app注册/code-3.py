import os
import re
import copy
import json
import base64
import datetime
import string
import random
import time
import hashlib
import ctypes
from base64 import b64encode
from urllib.parse import quote_plus, quote
from urllib.parse import urlsplit

import requests
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from Crypto.Cipher import PKCS1_v1_5, AES


class BiliBili(object):
    def __init__(self, proxy_dict):
        self.proxy_dict = proxy_dict

        self.session = requests.Session()
        self.session.proxies = proxy_dict

        self.build_brand = "HUAWEI"
        self.build_model = 'Mate 10 Pro'
        self.wifi_mac = self.create_random_mac().upper()
        self.device_id = self.create_device_id(self.wifi_mac)
        self.buvid = self.create_buvid_by_wifi()
        self.android_id = self.create_random_mac(sep="").lower()
        self.session_id = self.create_session_id()

        self.build_fingerprint = "OnePlus/OnePlus2/OnePlus2:6.0.1/MMB29M/1447841200:user/release-keys"
        self.build_display = "V417IR release-keys"

        self.fp_local = self.create_local(self.buvid, self.build_model, "")
        self.fp_remote = self.create_local(self.buvid, self.build_model, "")

        self.app_first_run_time = str(int(time.time()) - random.randint(0, 24 * 60 * 60))  # fts
        self.ts = str(int(time.time() - 10))

    def create_random_mac(self, sep=":"):
        """ 随机生成mac地址 """

        def mac_same_char(mac_string):
            v0 = mac_string[0]
            index = 1
            while index < len(mac_string):
                if v0 != mac_string[index]:
                    return False
                index += 1
            return True

        data_list = []
        for i in range(1, 7):
            part = "".join(random.sample("0123456789ABCDEF", 2))
            data_list.append(part)
        mac = sep.join(data_list)

        if not mac_same_char(mac) and mac != "00:90:4C:11:22:33":
            return mac

        return self.create_random_mac(sep)

    def create_device_id(self, mac):
        """
        根据mac地址生成 3.device_id
        :param mac: 传入参数的格式是 00:00:00:00:00
        :return:
        """

        def gen_sn():
            return "".join(random.sample("123456789" + string.ascii_lowercase, 10))

        def base64_encrypt(data_string):
            data_bytes = bytearray(data_string.encode('utf-8'))
            data_bytes[0] = data_bytes[0] ^ (len(data_bytes) & 0xFF)
            for i in range(1, len(data_bytes)):
                data_bytes[i] = (data_bytes[i - 1] ^ data_bytes[i]) & 0xFF
            res = base64.encodebytes(bytes(data_bytes))
            return res.strip().strip(b"==").decode('utf-8')

        # 1. 生成mac地址（保证mac中的每个元素是不重复的，例如：0000000000)
        mac_str = mac

        # 2. 去除IP地址中的符号，只保留 48e1e828e02e（变小写）
        mac_str = re.sub("[^0-9A-Fa-f]", "", mac_str)
        mac_str = mac_str.lower()

        # 3. 获取手续序列号
        sn = gen_sn()

        # 4. 拼接并进行base64加密
        total_string = "{}|||{}".format(mac_str, sn)
        return base64_encrypt(total_string)

    def create_buvid_by_wifi(self):
        """
            基于wifi mac地址生成buvid （ B站app中有四种获取buvid的方式：设备ID、wifi mac地址、3.device_id、uuid ）
        """
        md5 = hashlib.md5()
        md5.update(self.wifi_mac.encode('utf-8'))
        v0_1 = md5.hexdigest()
        return "XY{}{}{}{}".format(v0_1[2], v0_1[12], v0_1[22], v0_1).upper()

    def create_session_id(self):
        # return "".join([hex(item)[2:] for item in random.randbytes(4)])
        return "".join([hex(random.randint(1, 255))[2:] for i in range(4)])

    def create_heart_beat_session_id(self):
        def int_overflow(val):
            maxint = 2147483647
            if not -maxint - 1 <= val <= maxint:
                val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
            return val

        def unsigned_right_shitf(n, i):
            # 数字小于0，则转为32位无符号uint
            if n < 0:
                n = ctypes.c_uint32(n).value
            # 正常位移位数是为正数，但是为了兼容js之类的，负数就右移变成左移好了
            if i < 0:
                return -int_overflow(n << abs(i))
            # print(n)
            return int_overflow(n >> i)

        arg0 = str(int(time.time() * 1000)) + str(random.randint(1, 1000000));
        # sha1加密
        hash_object = hashlib.sha1()
        hash_object.update(arg0.encode('utf-8'))
        arg7 = hash_object.digest()
        v8 = [-1 for i in range(len(arg7) * 2)]
        v0 = len(arg7)
        v1 = 0
        v2 = 0
        while v1 < v0:
            v3 = arg7[v1]
            v4 = v2 + 1
            v5 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
            index = unsigned_right_shitf(v3, 4) & 15
            v8[v2] = v5[index]
            v2 = v4 + 1
            v8[v4] = v5[v3 & 15]
            # ++v1
            v1 += 1

        data = "".join(v8)
        return data.lower()

    def create_local(self, buvid, phone_model, phone_band):
        """
        fp_local和fp_remote都是用这个算法来生成的，在手机初始化阶段生成 fp_local，
        :param buvid: 根据算法生成的buvid，例如："XYBA4F3B2789A879EA8AEEDBE2E4118F78303"
        :param phone_model:  手机型号modal，例如："Mate 10 Pro"
        :param phone_band:  手机品牌band，在模拟器上是空字符串（我猜是程序员想要写成 brand ）哈哈哈哈
        :return:
        """

        def a_b(arg8):
            v3 = 0
            v4 = 60
            v0_1 = 2
            v5 = 0
            while True:
                v6 = arg8[v3:v3 + 2]
                v5 += int(v6, base=16)
                if v3 != v4:
                    v3 += v0_1
                    continue
                break
            data = "%02x" % (v5 % 0x100,)
            return data

        def misc_helper_kt(data_bytes):
            data_list = []
            v7 = len(data_bytes)
            v0 = 0
            while v0 < v7:
                v2 = data_bytes[v0]
                data_list.append("%02x" % v2)
                v0 += 1
            return ''.join(data_list)

        data_string = "{}{}{}".format(buvid, phone_model, phone_band)
        hash_object = hashlib.md5()
        hash_object.update(data_string.encode('utf-8'))
        data = hash_object.digest()

        arg1 = misc_helper_kt(data)
        arg2 = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        # arg3 = misc_helper_kt(random.randbytes(8))
        arg3 = misc_helper_kt([random.randint(1, 255) for i in range(8)])

        part_string = "{}{}{}".format(arg1, arg2, arg3)
        return part_string + a_b(part_string)

    def get_param_sign_s(self, param_dict):
        """
        :param param_dict: 要签名的参数字典
        :return:
        """
        ordered_string = "&".join(["{}={}".format(key, param_dict[key]) for key in sorted(param_dict.keys())])
        encrypt_string = ordered_string + "560c52ccd288fed045859ed18bffd973"
        obj = hashlib.md5(encrypt_string.encode('utf-8'))
        sign = obj.hexdigest()

        return "{}&sign={}".format(ordered_string, sign)

    def get_param_sign_so(self, param_dict):
        """
        :param param_dict: 要签名的参数字典
        :return:
        """
        ordered_string = "&".join(["{}={}".format(key, param_dict[key]) for key in sorted(param_dict.keys())])
        encrypt_string = ordered_string + "60698ba2f68e01ce44738920a0ffe768"
        obj = hashlib.md5(encrypt_string.encode('utf-8'))
        sign = obj.hexdigest()
        return "{}&sign={}".format(ordered_string, sign)

    def step_send_sms(self, region, mobile):
        data_dict = {
            "appkey": "bca7e84c2d947ac6",
            "build": "6240300",
            "c_locale": "zh_CN",
            "channel": "xxl_gdt_wm_253",
            "cid": region,  # 1 86
            "mobi_app": "android",
            "platform": "android",
            "s_locale": "zh_CN",
            "tel": mobile,
            "ts": int(time.time()),
        }
        total_body_string = self.get_param_sign_so(data_dict)
        res = self.session.post(
            url="https://passport.bilibili.com/x/passport-login/sms/send",
            data=total_body_string,
            headers={
                "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/MI 6 Plus mobi_app/android build/6240300 channel/xxl_gdt_wm_253 innerVer/6240300 osVer/6.0.1 network/2",
                "buvid": self.buvid,
                "env": "prod",
                "content-type": "application/x-www-form-urlencoded; charset=utf-8"
            }
        )
        # {'code': -3, 'message': 'API校验密匙错误', 'ttl': 1}
        # {"code":0,"message":"0","ttl":1,"data":{"is_new":false,"captcha_key":"3d882b573606ab046694a18189ba88c1","recaptcha_url":""}}
        # {'code': 0, 'message': '0', 'ttl': 1, 'data': {'is_new': False, 'captcha_key': '', 'recaptcha_url': 'https://www.bilibili.com/h5/project-msg-auth/verify?ct=geetest&recaptcha_token=5292e0ad8d194bb3807ad91f5fa43a49&gee_gt=1c0ea7c7d47d8126dda19ee3431a5f38&gee_challenge=213a5cc53b916db7abd1fd53dd6815ed&hash=c1940122a172e284e51421d137c2501d'}}
        data_dict = res.json()
        recaptcha_url = data_dict['data']['recaptcha_url']
        if not recaptcha_url:
            return False, data_dict
        v1 = urlsplit(recaptcha_url)
        data_dict = {item.split("=")[0]: item.split("=")[1] for item in v1.query.split("&")}
        return True, data_dict

    def step_send_sms_geetest(self, region, mobile, gee_challenge, gee_validate, recaptcha_token):

        data_dict = {
            "appkey": "bca7e84c2d947ac6",
            "build": "6240300",
            "c_locale": "zh_CN",
            "channel": "xxl_gdt_wm_253",
            "cid": region,  # 1 86
            "gee_challenge": gee_challenge,
            "gee_seccode": "{}%7Cjordan".format(gee_validate),
            "gee_validate": gee_validate,
            "mobi_app": "android",
            "platform": "android",
            "recaptcha_token": recaptcha_token,
            "s_locale": "zh_CN",
            "tel": mobile,
            "ts": int(time.time()),
        }

        total_body_string = self.get_param_sign_so(data_dict)
        # print('=====发短信字典：', total_body_string)
        res = self.session.post(
            url="https://passport.bilibili.com/x/passport-login/sms/send",
            data=total_body_string,
            headers={
                "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/MI 6 Plus mobi_app/android build/6240300 channel/xxl_gdt_wm_253 innerVer/6240300 osVer/6.0.1 network/2",
                "buvid": self.buvid,
                "env": "prod",
                "content-type": "application/x-www-form-urlencoded; charset=utf-8"
            }
        )
        # {"code":0,"message":"0","ttl":1,"data":{"is_new":false,"captcha_key":"3d882b573606ab046694a18189ba88c1","recaptcha_url":""}}
        # {'code': 86200, 'message': '短信请求过快，请60秒后重试', 'ttl': 1, 'data': {'is_new': True, 'captcha_key': '', 'recaptcha_url': ''}}
        data_dict = res.json()

        print("3.极验-发短信：", data_dict)
        if data_dict['code'] == 86200:
            print(data_dict['message'])
            return False

        self.captcha_key = data_dict['data']['captcha_key']
        self.is_new = data_dict['data']['is_new']
        return True


def get_proxy_dict():
    key = "BKA3YZD9"  # 用户key
    passwd = "885D61A4CBF8"  # 用户密码

    res = requests.get(
        url="https://proxy.qg.net/allocate?Key=BKA3YZD9&Num=1&AreaId=330700&DataFormat=json&DataSeparator=&Detail=0"
    )
    host = res.json()['Data'][0]['host']  # 121.29.81.215:52001

    # 账密模式
    proxy = 'http://{}:{}@{}'.format(key, passwd, host)
    return {"http": proxy, "https": proxy}


def run():
    region = "1"
    mobile = "5813346981"
    proxy_dict = get_proxy_dict()
    bili = BiliBili(proxy_dict)
    need_geetest, gee_dict = bili.step_send_sms(region, mobile)
    print("1.正常发短信：", gee_dict)

    if gee_dict.get("code") == 86200:
        print(gee_dict['message'])  # 操作频繁
        return

    if need_geetest:
        from geetest.v3.gee import do_geetest
        gee_challenge = gee_dict['gee_challenge']
        recaptcha_token = gee_dict['recaptcha_token']

        # {'success': 1, 'message': 'success', 'validate': '4ae92722bbeee2725a9c52b5ba1629d1', 'score': '2'} 86f4c93ec67bb595f38dd5ecf2b0115chy
        gee_res_dict, gee_challenge = do_geetest(gee_challenge, gee_dict['gee_gt'], proxy_dict)

        gee_validate = gee_res_dict['validate']
        print("2.极验-验证", gee_res_dict, gee_challenge)

        status = bili.step_send_sms_geetest(region, mobile, gee_challenge, gee_validate, recaptcha_token)
        print(status)


if __name__ == '__main__':
    run()
