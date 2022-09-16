import json
import os
import random
import time
from hashlib import md5

import requests


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
        self.cookie_info = None
        self.cookie_dict = None
        self.token_info = None

        self.initialize()

        self.session = requests.session()
        self.session.proxies = self.get_proxy_dict()

    @staticmethod
    def get_proxy_dict():
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

    def initialize(self):
        with open(self.file_path, mode="r", encoding="utf-8") as f:
            data_dict = json.load(f)
        for k, v in data_dict.items():
            setattr(self, k, v)
        self.cookie_dict = {item["name"]: item["value"] for item in self.cookie_info["cookies"]}

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

    def set_name(self):
        data_dict = {
            'access_key': self.token_info['access_token'],
            "appkey": "1d8b6e7d45233436",
            'csrf': self.cookie_dict["bili_jct"],
            "statistics": "%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%226.24.0%22%2C%22abtest%22%3A%22%22%7D",
            "ts": int(time.time()),
            "uname": "{}hello{}".format(random.randint(100, 999), random.randint(100, 999))
        }

        data_string = self.get_param_sign_so(data_dict)
        resp = self.session.post(
            url="https://api.bilibili.com/x/member/app/uname/update",
            data=data_string,
            headers={
                "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/21091116AC mobi_app/android build/6240300 channel/xxl_gdt_wm_253 innerVer/6240300 osVer/12 network/2",
                "buvid": self.buvid,
                'x-csrf-token': self.cookie_dict["bili_jct"],
                "referer": "https://www.bilibili.com/h5/newbie/basic-1?score=0",
                "native_api_from": 'h5',
                "content-type": "application/x-www-form-urlencoded; charset=utf-8"
            },
            cookies=self.cookie_dict
        )

        res_dict = resp.json()
        print("设置名字=>", res_dict)
        code = res_dict["code"]
        if code == 0:
            return True

    def set_avatar(self):
        name_list = os.listdir("images")
        name = random.choice(name_list)
        file_path = os.path.join("images", name)

        data_dict = {
            'access_key': self.token_info['access_token'],
            "appkey": "1d8b6e7d45233436",
            "build": "6240300",
            "c_locale": "zh_CN",
            "channel": "xxl_gdt_wm_253",
            "mobi_app": "android",
            "platform": "android",
            "s_locale": "zh_CN",
            "statistics": "%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%226.24.0%22%2C%22abtest%22%3A%22%22%7D",
            "ts": int(time.time())
        }

        param_string = self.get_param_sign_s(data_dict)
        resp = self.session.post(
            url="https://api.bilibili.com/x/member/app/face/update?{}".format(param_string),
            files={"face": open(file_path, 'rb')},
            headers={
                "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/21091116AC mobi_app/android build/6240300 channel/xxl_gdt_wm_253 innerVer/6240300 osVer/12 network/2",
                "buvid": self.buvid,
                'fp_local': self.fp_local,
                'fp_remote': self.fp_remote,
                "device-id": self.device_id,
                "app-key": 'android',
                "env": 'prod',
                'session_id': self.session_id,
                # 'content-type': "multipart/form-data; boundary={}".format(str(uuid.uuid4())),
            },
        )
        print("设置头像=>", resp.json())

    def get_mine(self):
        data_dict = {
            'access_key': self.token_info['access_token'],
            "appkey": "1d8b6e7d45233436",
            "build": "6240300",
            "c_locale": "zh_CN",
            "channel": "xxl_gdt_wm_253",
            "mobi_app": "android",
            "platform": "android",
            "s_locale": "zh_CN",
            "statistics": "%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%226.24.0%22%2C%22abtest%22%3A%22%22%7D",
            "ts": int(time.time())
        }

        param_string = self.get_param_sign_s(data_dict)
        resp = self.session.get(
            url="https://app.bilibili.com/x/v2/account/mine?{}".format(param_string),
            headers={
                "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/21091116AC mobi_app/android build/6240300 channel/xxl_gdt_wm_253 innerVer/6240300 osVer/12 network/2",
                "buvid": self.buvid,
                'fp_local': self.fp_local,
                'fp_remote': self.fp_remote,
                "device-id": self.device_id,
                "app-key": 'android',
                "env": 'prod',
                'session_id': self.session_id
            },
            cookies=self.cookie_dict
        )
        # print(res.text)
        # {"code":0,"message":"0","ttl":1,"data":{"mid":1283831984,"name":"1122哈哈哈333","show_name_gui}}
        print("获取个人信息=>", resp.json())


def run():
    file_path = "5813346972.txt"

    bili = Bilibili(file_path)
    # 设置名字 [app] + [web+cookie]
    bili.set_name()
    # 上传头像 [app] + [web+cookie]
    bili.set_avatar()
    # 获取个人信息 [app] + [web+cookie]
    bili.get_mine()
    bili.session.close()


if __name__ == '__main__':
    run()
