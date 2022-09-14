import json
import time
from hashlib import md5
from urllib.parse import quote_plus

import ddddocr
import requests


class Bilibili(object):
    def __init__(self, file_path):
        self.cookie_dict = None
        self.answer_list = None
        self.question_id = None
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

    def status(self):
        data_dict = {
            "access_key": self.token_info["access_token"],
            "appkey": "1d8b6e7d45233436",
            "build": "6240300",
            "channel": "xxl_gdt_wm_253",
            "mobi_app": "android",
            "platform": "android",
            "re_src": "0",
            "statistics": quote_plus(
                json.dumps({"appId": 1, "platform": 3, "version": "6.24.0", "abtest": ""}, separators=(",", ":"))),
            "ts": int(time.time()),
        }
        param_string = self.get_param_sign_so(data_dict)

        resp = self.session.get(
            url="https://api.bilibili.com/x/answer/v4/status?{}".format(param_string.encode('utf-8')),
            headers={
                "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/21091116AC mobi_app/android build/6240300 channel/xxl_gdt_wm_253 innerVer/6240300 osVer/12 network/2",
                "buvid": self.buvid,
                "referer": "https://www.bilibili.com/h5/newbie/entry?spm_id=main.my-page.answer.0&navhide=1&native.theme=1",
                "native_api_from": 'h5',
                "content-type": "application/json"
            },
            cookies={item['name']: item['value'] for item in self.cookie_info['cookies']}
        )
        # {'hid': 1660720523461603, 'mid': 1994769663, 'score': 1, 'status': 2, 'number': 1, 'result': 'failed', 'stage': 'base', 'version': 'v4', 'start_time': 1660720523, 'first_answer': 1, 'progress': '2', 'text': '继续答题', 'url': 'https://www.bilibili.com/h5/newbie/entry?navhide=1', 'in_reg_audit': False, 'edition': 2, 'rewards': None}
        return resp.json()

    def base(self):
        data_dict = {
            'access_key': self.token_info['access_token'],
            "appkey": "1d8b6e7d45233436",
            "area": "0",
            "build": "6240300",
            "channel": "xxl_gdt_wm_253",
            "image_version": "v",
            "mobi_app": "android",
            "platform": "h5",
            "re_src": "0",
            "statistics": quote_plus(
                json.dumps({"appId": 1, "platform": 3, "version": "6.24.0", "abtest": ""}, separators=(",", ":"))),
            "ts": int(time.time()),
        }
        param_string = self.get_param_sign_so(data_dict)
        resp = self.session.get(
            url="https://api.bilibili.com/x/answer/v4/base?{}".format(param_string),
            headers={
                "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/21091116AC mobi_app/android build/6240300 channel/xxl_gdt_wm_253 innerVer/6240300 osVer/12 network/2",
                "buvid": self.buvid,
                "referer": "https://www.bilibili.com/h5/newbie/basic-1?score=0",
                "native_api_from": 'h5',
                "content-type": "application/json"
            },
            cookies={item['name']: item['value'] for item in self.cookie_info['cookies']}
        )

        # {'question': {'id': 6649, 'number': 1, 'q_height': 76.8, 'q_coord_y': 0, 'image': 'https://i0.hdslb.com/bfs/member/729b1a328a8639555989d0c69f20ec63.png', 'from': '', 'options': [{'number': 1, 'high': 42, 'coord_y': 76.8, 'hash': '916ca6a13247748c0f134620d6f2e640'}, {'number': 2, 'high': 42, 'coord_y': 118.8, 'hash': 'ea4b4bc03737435233b0d3276e236594'}], 'type_id': 36, 'type_name': '小电视校长', 'type_image': 'https://i0.hdslb.com/bfs/face/7b67c0c0da64a6ab059ff49bb0d4b92988b91806.png'}}
        # {'code': 41020, 'message': '用户基础题已通过', 'ttl': 1}
        # print(res.json())
        res_dict = resp.json()["data"]
        print(res_dict)
        self.question_id = res_dict["question"]["id"]
        self.answer_list = [item["hash"] for item in res_dict["question"]["options"]]

    def base_check(self):
        for ans_hash in self.answer_list:
            data_dict = {
                'access_key': self.token_info['access_token'],
                "ans_hash": ans_hash,
                "appkey": "1d8b6e7d45233436",
                "area": "0",
                "build": "6240300",
                "channel": "xxl_gdt_wm_253",
                'csrf': self.cookie_dict["bili_jct"],
                "mobi_app": "android",
                "platform": "h5",
                "question_id": self.question_id,
                "re_src": "0",
                "statistics": quote_plus(
                    json.dumps({"appId": 1, "platform": 3, "version": "6.24.0", "abtest": ""}, separators=(",", ":"))),
                "ts": int(time.time()),
            }
            data_string = self.get_param_sign_so(data_dict)
            resp = self.session.get(
                url="https://api.bilibili.com/x/answer/v4/base/check",
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
            # print(res_dict)
            if res_dict['data']['passed']:
                return

    def get_captcha(self):
        data_dict = {
            'access_key': self.token_info['access_token'],
            "appkey": "1d8b6e7d45233436",
            "area": "0",
            "build": "6240300",
            "channel": "xxl_gdt_wm_253",
            "mobi_app": "android",
            "platform": "android",
            "re_src": "0",
            "statistics": "%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%226.24.0%22%2C%22abtest%22%3A%22%22%7D",
            "ts": int(time.time()),
        }

        param_string = self.get_param_sign_so(data_dict)
        resp = self.session.get(
            url="https://api.bilibili.com/x/answer/v4/captcha?{}".format(param_string),
            headers={
                "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/21091116AC mobi_app/android build/6240300 channel/xxl_gdt_wm_253 innerVer/6240300 osVer/12 network/2",
                "buvid": self.buvid,
                "referer": "https://www.bilibili.com/h5/newbie/basic-1?score=0",
                "native_api_from": 'h5',
                "content-type": "application/json"
            },
            cookies={item['name']: item['value'] for item in self.cookie_info['cookies']}
        )
        return resp.json()['data']['token'], resp.json()['data']['url']

    def get_image_code(self, url):
        resp = self.session.get(
            url=url,
            headers={
                "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/21091116AC mobi_app/android build/6240300 channel/xxl_gdt_wm_253 innerVer/6240300 osVer/12 network/2",
                "buvid": self.buvid,
                "referer": "https://www.bilibili.com/h5/newbie/basic-1",
                "native_api_from": 'h5',
                "content-type": "application/json",
                "x-requested-with": "tv.danmaku.bili"
            },
            cookies={item['name']: item['value'] for item in self.cookie_info['cookies']}
        )
        ocr = ddddocr.DdddOcr(show_ad=False)
        img_code = ocr.classification(resp.content).strip()
        return img_code

    def captcha_check(self, token, image_code):
        data_dict = {
            'access_key': self.token_info['access_token'],
            "appkey": "1d8b6e7d45233436",
            "area": "0",
            "bilibili_code": image_code,
            "bilibili_token": token,
            "build": "6240300",
            "channel": "xxl_gdt_wm_253",
            'csrf': self.cookie_dict["bili_jct"],
            'geetest_challenge': "",
            'geetest_seccode': "",
            'geetest_validate': "",
            "mobi_app": "android",
            "platform": "android",
            "re_src": "0",
            "statistics": quote_plus(
                json.dumps({"appId": 1, "platform": 3, "version": "6.24.0", "abtest": ""}, separators=(",", ":"))),
            "ts": int(time.time()),
            'type': "bilibili",
            'types': "",
        }
        data_string = self.get_param_sign_so(data_dict)

        resp = self.session.get(
            url="https://api.bilibili.com/x/answer/v4/captcha/check",
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
        if res_dict["code"] == 0:
            return True

    def extra(self):
        data_dict = {
            'access_key': self.token_info['access_token'],
            "appkey": "1d8b6e7d45233436",
            "area": "0",
            "build": "6240300",
            "channel": "xxl_gdt_wm_253",
            "image_version": "v",
            "mobi_app": "android",
            "platform": "h5",
            "re_src": "0",
            "statistics": quote_plus(
                json.dumps({"appId": 1, "platform": 3, "version": "6.24.0", "abtest": ""}, separators=(",", ":"))),
            "ts": int(time.time()),
        }
        param_string = self.get_param_sign_so(data_dict)
        resp = self.session.get(
            url="https://api.bilibili.com/x/answer/v4/extra?{}".format(param_string),
            headers={
                "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/21091116AC mobi_app/android build/6240300 channel/xxl_gdt_wm_253 innerVer/6240300 osVer/12 network/2",
                "buvid": self.buvid,
                "referer": "https://www.bilibili.com/h5/newbie/basic-1?score=0",
                "native_api_from": 'h5',
                "content-type": "application/json"
            },
            cookies={item['name']: item['value'] for item in self.cookie_info['cookies']}
        )
        # {'question': {'id': 6649, 'number': 1, 'q_height': 76.8, 'q_coord_y': 0, 'image': 'https://i0.hdslb.com/bfs/member/729b1a328a8639555989d0c69f20ec63.png', 'from': '', 'options': [{'number': 1, 'high': 42, 'coord_y': 76.8, 'hash': '916ca6a13247748c0f134620d6f2e640'}, {'number': 2, 'high': 42, 'coord_y': 118.8, 'hash': 'ea4b4bc03737435233b0d3276e236594'}], 'type_id': 36, 'type_name': '小电视校长', 'type_image': 'https://i0.hdslb.com/bfs/face/7b67c0c0da64a6ab059ff49bb0d4b92988b91806.png'}}
        # {'code': 41020, 'message': '用户基础题已通过', 'ttl': 1}
        # {'code': 41051, 'message': '用户答题验证码未通过', 'ttl': 1}
        res_dict = resp.json()
        if res_dict["code"] == 41051:
            while True:
                token, url = self.get_captcha()
                image_code = self.get_image_code(url)
                print(image_code)
                if self.captcha_check(token, image_code):
                    return
        res_dict = resp.json()["data"]
        self.question_id = res_dict["question"]["id"]
        self.answer_list = [item["hash"] for item in res_dict["question"]["options"]]

    def extra_check(self):
        for ans_hash in self.answer_list:
            data_dict = {
                'access_key': self.token_info['access_token'],
                "ans_hash": ans_hash,
                "appkey": "1d8b6e7d45233436",
                "area": "0",
                "build": "6240300",
                "channel": "xxl_gdt_wm_253",
                'csrf': self.cookie_dict["bili_jct"],
                "mobi_app": "android",
                "platform": "h5",
                "question_id": self.question_id,
                "re_src": "0",
                "statistics": quote_plus(
                    json.dumps({"appId": 1, "platform": 3, "version": "6.24.0", "abtest": ""}, separators=(",", ":"))),
                "ts": int(time.time()),
            }
            data_string = self.get_param_sign_so(data_dict)
            resp = self.session.get(
                url="https://api.bilibili.com/x/answer/v4/extra/check",
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
            if res_dict["data"]["passed"]:
                return


def run():
    file_path = "5813346972.txt"

    bili = Bilibili(file_path)

    while True:
        time.sleep(1)
        info_dict = bili.status()
        print(info_dict)
        score = info_dict["data"]["score"]
        print("得分：", score)
        if score >= 60:
            break
        if info_dict["data"]["stage"] == "base":
            # 获取question_id和问题答案hash值
            bili.base()
            # 检查是否回答正确
            bili.base_check()
        elif info_dict["data"]["stage"] == "extra":
            if not bili.extra():
                # 图片验证成功，继续答题
                continue
            bili.extra_check()
    bili.session.close()
    print("答题成功")


if __name__ == '__main__':
    run()
