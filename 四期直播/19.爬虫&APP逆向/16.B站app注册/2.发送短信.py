import re
import time
import json
import string
import random
import base64
import requests
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from urllib.parse import quote_plus, urlsplit
from hashlib import md5, sha256, sha1


class Bilibili(object):
    """
        1. 签名时，自动会生成ts字段
        2. ts比当前时间小 1000s
    """

    def __init__(self, aid="", bvid="", cid="", duration=0):
        self.start_ts = None
        self.heart_beat_session_id = None
        self.aid, self.bvid, self.cid, self.duration = aid, bvid, cid, duration

        self.build_brand = "Redmi"
        self.build_model = "2019111AC"

        self.wifi_mac = self.create_random_mac().upper()
        self.device_id = self.create_device_id(self.wifi_mac)  # did
        self.buvid = self.create_buvid_by_wifi()
        self.session_id = self.create_session_id()
        self.fp_local = self.create_local(self.buvid, self.build_model, "")
        self.fp_remote = self.create_local(self.buvid, self.build_model, "")

        self.app_first_run_time = str(int(time.time()) - random.randint(0, 24 * 60 * 60))  # fts
        self.ts = str(int(time.time() - 10))

        self.session = requests.session()
        # self.session.proxies = self.get_proxy_dict()

    @staticmethod
    def get_proxy_dict():
        key = "tps150.kdlapi.com:15818"
        passwd = "t12678079599196"
        host = "gbtn0lkl"
        return {
            "http": 'http://{}:{}@{}'.format(key, passwd, host),
            "https": 'https://{}:{}@{}'.format(key, passwd, host)
        }

    @staticmethod
    def gen_sn():
        """
        随机生成一个10位字符串
        :return: string
        """
        return "".join(random.sample("123456789" + string.ascii_lowercase, 10))

    @staticmethod
    def a_b(arg8):
        v3, v4, v0_1, v5 = 0, 60, 2, 0

        while True:
            v6 = arg8[v3: v3 + 2]
            v5 += int(v6, base=16)
            if v3 != v4:
                v3 += v0_1
                continue
            break
        xx = "%02x" % (v5 % 0x100,)
        return xx

    @staticmethod
    def misc_helper_kt(data_bytes):
        data_list = []
        v0, v7 = 0, len(data_bytes)
        while v0 < v7:
            v2 = data_bytes[v0]
            data_list.append("%02x" % v2)
            v0 += 1
        return "".join(data_list)

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
    def aes_encrypt(data_string):
        KEY = "fd6b639dbcff0c2a1b03b389ec763c4b"
        IV = "77b07a672d57d64c"

        aes = AES.new(
            key=KEY.encode("utf-8"),
            mode=AES.MODE_CBC,
            iv=IV.encode("utf-8")
        )
        raw = pad(data_string.encode("utf-8"), 16)
        return aes.encrypt(raw)

    @staticmethod
    def base64_encrypt(data_string):
        data_bytes = bytearray(data_string.encode('utf-8'))
        data_bytes[0] = data_bytes[0] ^ (len(data_bytes) & 0xFF)
        for i in range(1, len(data_bytes)):
            data_bytes[i] = (data_bytes[i - 1] ^ data_bytes[i]) & 0xFF
        res = base64.encodebytes(bytes(data_bytes))
        return res.strip().strip(b"==").decode('utf-8')

    def create_random_mac(self, sep=":"):
        """
        随机生成mac地址
        :param sep: 连接符
        :return: string
        """
        data_list = []
        for i in range(1, 7):
            part = "".join(random.sample("0123456789ABCDEF", 2))
            data_list.append(part)
        mac = sep.join(data_list)
        return mac

    def create_device_id(self, mac):
        """
        根据mac地址生成 device_id
        :param mac: mac地址
        :return: string
        """
        # 去除IP地址中的符号，只保留数字和字母，转成小写
        mac_str = mac
        mac_str = re.sub("[^0-9A-Fa-f]", "", mac_str)
        mac_str = mac_str.lower()

        # 获取手机序列号
        sn = self.gen_sn()

        # 拼接进行base64加密
        data_string = f"{mac_str}|||{sn}"
        return self.base64_encrypt(data_string)

    def create_buvid_by_wifi(self):
        """
        B站有四种获取buvid的方式：设备ID、WiFi mac地址、device_id、uuid
        采用wifi mac地址生成buvid
        :return: string
        """
        v = self.md5_encrypt(self.wifi_mac)
        return f"XY{v[2]}{v[12]}{v[22]}{v}".upper()

    def create_session_id(self):
        """
        随机生成四个字节字符串
        :return: string
        """
        # return "".join([hex(item)[2:] for item in random.randbytes(4)])
        return "".join([str.rjust(hex(random.randint(0, 255))[2:], 2, "0") for _ in range(4)])

    def create_local(self, buvid, phone_model, phone_band):
        """
        fp_local和fp_remote都是根据这个算法生成的，在手机初始化阶段生成fp_local
        :param buvid: 根据算法生成的buvid
        :param phone_model: 手机型号
        :param phone_band: 手机品牌
        :return: string
        """
        data_string = f"{buvid}{phone_model}{phone_band}"
        data = self.md5_encrypt(data_string, True)
        arg1 = self.misc_helper_kt(data)
        arg2 = datetime.now().strftime("%Y%m%d%H%M%S")
        # arg3 = self.misc_helper_kt(random.randbytes(8))
        arg3 = self.misc_helper_kt([random.randint(0, 255) for _ in range(8)])
        str2 = f"{arg1}{arg2}{arg3}"
        return str2 + self.a_b(str2)

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

    def step_send_sms(self, region, mobile):
        form_dict = {
            "appkey": "bca7e84c2d947ac6",
            "build": "6240300",
            "c_locale": "zh_CN",
            "channel": "xxl_gdt_wm_253",
            "cid": region,
            "mobi_app": "android",
            "platform": "android",
            "s_locale": "zh_CN",
            "tel": mobile,
            "ts": int(time.time()),
        }

        body_string = self.get_param_sign_so(form_dict)

        resp = self.session.post(
            url="https://passport.bilibili.com/x/passport-login/sms/send",
            data=body_string,
            headers={
                "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/21091116AC mobi_app/android build/6240300 channel/xxl_gdt_wm_253 innerVer/6240300 osVer/12 network/2",
                "buvid": self.buvid,
                "env": "prod",
                "content-type": "application/x-www-form-urlencoded; charset=utf-8"
            }
        )

        # print(resp.json())  # {'code': 0, 'message': '0', 'ttl': 1, 'data': {'is_new': True, 'captcha_key': 'eea37033a762f497a3ca57521f9751b1', 'recaptcha_url': ''}}
        data_dict = resp.json()
        recaptcha_url = data_dict["data"]["recaptcha_url"]

        if not recaptcha_url:
            return False, data_dict

        # 需要滑动验证
        v1 = urlsplit(recaptcha_url)
        data_dict = {item.split("=")[0]: item.split("=")[1] for item in v1.query.split("&")}
        return True, data_dict


def run():
    bili = Bilibili()
    need_geetest, gee_dict = bili.step_send_sms("1", "5813346981")

    if gee_dict.get("code") == 86200:
        print(gee_dict["message"])  # 操作频繁
        return

    # if need_geetest:
        # from geetest.v3.gee import do_geetest
        #
        # gee_challenge = gee_dict["gee_challenge"]
        # recaptcha_token = gee_dict["recaptcha_token"]
        #
        # gee_res_dict, gee_challenge = do_geetest(gee_challenge, gee_dict["gee_gt"], bili.get_proxy_dict())
        #
        # print(gee_res_dict, gee_challenge)

        # 还需要再次发送短信


if __name__ == '__main__':
    run()
