import re
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
from geetest.v3.gee import do_geetest


class Bilibili(object):

    def __init__(self):
        self.cookie_info = None
        self.token_info = None
        self.code = None
        self.mid = None
        self.is_new = None
        self.captcha_key = None
        self.guest_id = None
        self.rsa_pub_key = None
        self.hash = None
        self.start_ts = None
        self.heart_beat_session_id = None

        self.build_brand = "Redmi"
        self.build_model = "2019111AC"
        self.build_fingerprint = "Redmi/evergo/evergo:12/SP1A.210812.016/V13.0.6.0.SGBCNXM:user/release-keys"
        self.build_display = "evergo-user 12 SP1A.210812.016 V13.0.6.0.SGBCNXM"

        self.wifi_mac = self.create_random_mac().upper()
        self.device_id = self.create_device_id(self.wifi_mac)  # did
        self.buvid = self.create_buvid_by_wifi()
        self.session_id = self.create_session_id()
        self.fp_local = self.create_local(self.buvid, self.build_model, "")
        self.fp_remote = self.create_local(self.buvid, self.build_model, "")
        self.android_id = self.create_random_mac(sep="").lower()

        self.app_first_run_time = str(int(time.time()) - random.randint(0, 24 * 60 * 60))  # fts
        self.ts = str(int(time.time() - 10))

        self.session = requests.session()
        self.session.proxies = self.get_proxy_dict()

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
    def create_random_string(count=16, sep=""):
        ca = string.digits + string.ascii_letters

        char_list = []
        for v2 in range(count):
            char = random.choice(ca)
            char_list.append(char)

        return sep.join(char_list)

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

    def step_web_key(self):
        param_dict = {
            "appkey": "1d8b6e7d45233436",
            "build": "6240300",
            "c_locale": "zh_CN",
            "channel": "xxl_gdt_wm_253",
            "mobi_app": "android",
            "platform": "android",
            "s_locale": "zh_CN",
            "statistics": quote_plus(
                json.dumps({"appId": 1, "platform": 3, "version": "6.24.0", "abtest": ""}, separators=(',', ':'))),
            "ts": int(time.time()),
        }

        query_string = self.get_param_sign_so(param_dict)
        resp = self.session.get(
            url=f"https://passport.bilibili.com/x/passport-login/web/key?{query_string}",
            headers={
                "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/21091116AC mobi_app/android build/6240300 channel/xxl_gdt_wm_253 innerVer/6240300 osVer/12 network/2",
                "buvid": self.buvid,
                'env': "prod",
                'app-key': "android",
                "content-type": "application/x-www-form-urlencoded; charset=utf-8"
            }
        )

        data_dict = resp.json()
        print("获取公钥", data_dict)

        self.hash = data_dict["data"]["hash"]
        self.rsa_pub_key = data_dict["data"]["key"]

    def step_passport_guest_reg_5(self):
        """
        游客注册，用于获取游客 guest_id
        :return:
        """
        device_info_dict = {
            "AndroidID": self.android_id,
            "BuildBrand": self.build_brand,
            "BuildDisplay": self.build_display,
            "BuildFingerprint": self.build_fingerprint,
            "BuildHost": "c4-xm-ota-bd055.bj",
            "Buvid": self.buvid,
            "DeviceType": "Android",
            "MAC": self.wifi_mac,
            "fts": self.app_first_run_time
        }

        # 根据这个字典信息生成dt 和 device_info （顺序不能乱）
        data_string = json.dumps(device_info_dict, separators=(",", ":"))
        random_string = self.create_random_string()

        device_info = self.aes_encrypt(data_string, random_string, random_string)
        dt = self.rsa_encrypt(random_string)

        body = {
            'appkey': "bca7e84c2d947ac6",
            'build': '6240300',
            "c_locale": "zh_CN",
            "channel": "xxl_gdt_wm_253",
            'device_info': device_info,
            'dt': quote_plus(dt),
            'mobi_app': 'android',
            'platform': 'android',
            's_local': 'zh_CN',
            'ts': int(time.time())
        }

        body_string = self.get_param_sign_so(body)
        resp = self.session.post(
            url="https://passport.bilibili.com/x/passport-user/guest/reg",
            data=body_string,
            headers={
                "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/21091116AC mobi_app/android build/6240300 channel/xxl_gdt_wm_253 innerVer/6240300 osVer/12 network/2",
                "buvid": self.buvid,
                "env": "prod",
                "content-type": "application/x-www-form-urlencoded; charset=utf-8"
            }
        )

        # 获取guest_id
        data_dict = resp.json()
        self.guest_id = str(data_dict["data"]["guest_id"])

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
        body_string = self.get_param_sign_so(data_dict)

        resp = self.session.post(
            url="https://passport.bilibili.com/x/passport-login/sms/send",
            data=body_string,
            headers={
                "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/MI 6 Plus mobi_app/android build/6240300 channel/xxl_gdt_wm_253 innerVer/6240300 osVer/6.0.1 network/2",
                "buvid": self.buvid,
                "env": "prod",
                "content-type": "application/x-www-form-urlencoded; charset=utf-8"
            }
        )

        # {"code":0,"message":"0","ttl":1,"data":{"is_new":false,"captcha_key":"3d882b573606ab046694a18189ba88c1","recaptcha_url":""}}
        # {'code': 86200, 'message': '短信请求过快，请60秒后重试', 'ttl': 1, 'data': {'is_new': True, 'captcha_key': '', 'recaptcha_url': ''}}
        data_dict = resp.json()
        print("极验-发短信：", data_dict)
        if data_dict['code'] == 86200:
            print(data_dict['message'])
            return False

        self.captcha_key = data_dict['data']['captcha_key']
        self.is_new = data_dict['data']['is_new']
        return True

    def step_login_sms(self, region, code, mobile):
        fingerprint_dict = {
            "aaid": "",
            "accessibility_service": "[\"com.android.settings/.accessibility.accessibilitymenu.AccessibilityMenuService\", \"com.google.android.marvin.talkback/.TalkBackService\", \"com.google.android.marvin.talkback/com.google.android.accessibility.accessibilitymenu.AccessibilityMenuService\", \"com.google.android.marvin.talkback/com.google.android.accessibility.selecttospeak.SelectToSpeakService\", \"com.google.android.marvin.talkback/com.android.switchaccess.SwitchAccessService\", \"com.miui.accessibility/.environment.sound.recognition.EnvSoundRecognitionService\", \"com.miui.accessibility/.voiceaccess.VoiceAccessAccessibilityService\", \"com.miui.accessibility/.haptic.HapticAccessibilityService\", \"com.miui.personalassistant/com.miui.voicesdk.VoiceAccessibilityService\", \"com.miui.securitycenter/com.miui.gamebooster.gbservices.AntiMsgAccessibilityService\", \"com.miui.securitycenter/com.miui.luckymoney.service.LuckyMoneyAccessibilityService\", \"com.miui.voiceassist/.accessibility.VoiceAccessibilityService\", \"com.sohu.inputmethod.sogou.xiaomi/com.sohu.inputmethod.flx.quicktype.QuickAccessibilityService\", \"com.xiaomi.gamecenter.sdk.service/com.xiaomi.gamecenter.sdk.ui.mifloat.process.DetectService\", \"bin.mt.plus/l.ۨۘۗ\", \"com.baidu.input_mi/com.baidu.acs.service.AcsService\", \"com.iflytek.inputmethod.miui/com.iflytek.libaccessibility.mi.FlyIMEAccessibilityService\", \"com.xiaomi.scanner/.qrcodeautoprocessing.MyAccessibilityService\"]",
            "adb_enabled": "1", "adid": "54f6ab6877163109",
            "androidapp20": "[\"1662212845000,com.miui.screenrecorder,0,2.12.5.20.1,21205201,1662212845000\", \"1662470057833,com.goplaycn.googleinstall,0,4.8.7,487,1662470057833\", \"1662268571364,com.che168.autotradercloud,0,2.8.5,247,1662268571364\", \"1662276074649,com.speedsoftware.rootexplorer,0,4.5.1,165,1662276074649\", \"1662470392004,com.v2ray.ang,0,1.1.12,254,1662470392004\", \"1662212850000,com.android.soundrecorder,0,1.9.84.9,109849,1662212850000\", \"1662212850000,com.baidu.input_mi,0,10.6.66.231,770,1662216577104\", \"1662212846000,com.xiaomi.mibrain.speech,0,1.4.2,37,1662212846000\", \"1662214820000,com.miui.huanji,0,3.9.4,30940,1662216636656\", \"1662502634225,com.shizhuang.duapp,0,4.84.0,436,1662502634225\", \"1662212846000,cn.wps.moffice_eng.xiaomi.lite,0,2.6.0,260,1662212846000\", \"1662212846000,com.mfashiongallery.emag,0,M922082400-S,2022082400,1662216876659\", \"1662217001657,bin.mt.plus,0,2.11.6,22082574,1662217001657\", \"1662212849000,com.miui.virtualsim,0,6.2.9,629,1662217082891\", \"1662214822000,com.duokan.phone.remotecontroller,0,6.4.2,6328,1662216638882\", \"1662474831437,org.sandroproxy.drony,0,1.3.154,154,1662474831437\", \"1662212847000,com.xiaomi.shop,0,5.9.1.20220809.r5,20220809,1662216608595\", \"1662470149700,com.google.android.gms,0,22.12.56 (190400-439724354),221256044,1662470149700\", \"1662470115498,com.google.android.gsf,0,12-7567768,31,1662470115498\", \"1662212850000,com.iflytek.inputmethod.miui,0,8.1.8001,8001,1662216612518\"]",
            "androidappcnt": 293,
            "androidsysapp20": "[\"1230768000000,com.mediatek.ims,1,12,31,1230768000000\", \"1230768000000,com.factory.mmigroup,1,2.1,3,1230768000000\", \"0,com.android.cts.priv.ctsshim,1,12-7552332,31,0\", \"1230768000000,com.miui.contentextension,1,2.5.64,20064,1230768000000\", \"1230768000000,com.android.internal.display.cutout.emulation.corner,1,1.0,1,1230768000000\", \"1230768000000,com.android.internal.display.cutout.emulation.double,1,1.0,1,1230768000000\", \"1230768000000,com.mediatek.autobootcontroller,1,12,31,1230768000000\", \"1230768000000,com.android.providers.telephony,1,12,31,1230768000000\", \"1230768000000,com.android.dynsystem,1,12,31,1230768000000\", \"1230768000000,com.miui.powerkeeper,1,4.2.00,40200,1230768000000\", \"1230768000000,com.goodix.fingerprint,1,1.0.04,4,1230768000000\", \"1230768000000,com.unionpay.tsmservice.mi,1,01.00.44,45,1662216969129\", \"1230768000000,com.android.providers.calendar,1,10.0.5.5,10000505,1230768000000\", \"1230768000000,com.miui.contentcatcher,1,1.0.002,2,1230768000000\", \"1230768000000,com.mediatek.telephony,1,12,31,1230768000000\", \"1230768000000,com.android.providers.media,1,12,1024,1230768000000\", \"1230768000000,com.milink.service,1,12.4.8.21,12040821,1662216836330\", \"1230768000000,com.miui.dmregservice,1,3.0,3,1230768000000\", \"1230768000000,com.android.networkstack.tethering.overlay,1,12,31,1230768000000\", \"1230768000000,com.android.internal.systemui.navbar.gestural_wide_back,1,1.0,1,1230768000000\"]",
            "app_id": "1", "app_version": "6.24.0", "app_version_code": "6240300",
            "apps": "[\"1662212845000,com.miui.screenrecorder,0,2.12.5.20.1,21205201,1662212845000\",\"1230768000000,com.mediatek.ims,1,12,31,1230768000000\",\"1230768000000,com.factory.mmigroup,1,2.1,3,1230768000000\",\"0,com.android.cts.priv.ctsshim,1,12-7552332,31,0\",\"1230768000000,com.miui.contentextension,1,2.5.64,20064,1230768000000\",\"1662470057833,com.goplaycn.googleinstall,0,4.8.7,487,1662470057833\",\"1230768000000,com.android.internal.display.cutout.emulation.corner,1,1.0,1,1230768000000\",\"1230768000000,com.android.internal.display.cutout.emulation.double,1,1.0,1,1230768000000\",\"1230768000000,com.mediatek.autobootcontroller,1,12,31,1230768000000\",\"1230768000000,com.android.providers.telephony,1,12,31,1230768000000\",\"1230768000000,com.android.dynsystem,1,12,31,1230768000000\",\"1230768000000,com.miui.powerkeeper,1,4.2.00,40200,1230768000000\",\"1230768000000,com.goodix.fingerprint,1,1.0.04,4,1230768000000\",\"1662268571364,com.che168.autotradercloud,0,2.8.5,247,1662268571364\",\"1230768000000,com.unionpay.tsmservice.mi,1,01.00.44,45,1662216969129\",\"1230768000000,com.android.providers.calendar,1,10.0.5.5,10000505,1230768000000\",\"1230768000000,com.miui.contentcatcher,1,1.0.002,2,1230768000000\",\"1230768000000,com.mediatek.telephony,1,12,31,1230768000000\",\"1230768000000,com.android.providers.media,1,12,1024,1230768000000\",\"1230768000000,com.milink.service,1,12.4.8.21,12040821,1662216836330\"]",
            "axposed": "false", "band": "MOLY.NR15.R3.MP.V29.5.P59,MOLY.NR15.R3.MP.V29.5.P59",
            "battery": 100, "batteryState": "BATTERY_STATUS_FULL", "biometric": "1",
            "biometrics": "touchid", "boot": "49588975", "brand": "Redmi", "brightness": "427",
            "bssid": "02:00:00:00:00:00", "btmac": "",
            "build_id": "evergo-user 12 SP1A.210812.016 V13.0.6.0.SGBCNXM",
            "buvid_local": self.buvid,
            "chid": "xxl_gdt_wm_253",
            "countryIso": "cn", "cpuCount": "8", "cpuFreq": "2000000",
            "cpuModel": "ARMv8 Processor rev 0 (v8l)", "cpuVendor": "ARM", "data_activity_state": "4",
            "data_connect_state": "0", "data_network_type": "0",
            "device_angle": "-0.7107677,-0.16320774,-0.13472752", "emu": "000",
            "files": "/data/user/0/tv.danmaku.bili/files", "first": "true", "free_memory": "5088047104",
            "fstorage": 222682894336,
            "fts": self.app_first_run_time,
            "gadid": "", "glimit": "", "gps_sensor": "1",
            "guest_id": self.guest_id,
            "guid": "45ed2e4d-2dab-43f9-bd3f-466da2e3ec1d",
            "gyroscope_sensor": "1", "imei": "", "is_root": "true",
            "kernel_version": "4.14.186-perf-gbed09115381c", "languages": "zh",
            "last_dump_ts": str(int(time.time() * 1000)),
            "light_intensity": "46.0", "linear_speed_sensor": "1",
            "mac": self.wifi_mac,
            "maps": "", "mem": "7999275008", "memory": "7999275008", "mid": "",
            "model": "21091116AC",
            "net": "[\"dummy0,fe80::60c8:f6ff:fef4:f894%dummy0,\", \"wlan0,fe80::7c62:5dff:fe66:7e62%wlan0,192.168.0.144,\", \"lo,::1,127.0.0.1,\", \"ccmni0,fe80::1b28:5932%ccmni0,2408:850c:823f:7915::1b28:5932,\"]",
            "network": "WIFI", "oaid": "", "oid": "46009", "os": "android", "osver": "12",
            "proc": "tv.danmaku.bili",
            "props": {"gsm.network.type": "LTE,Unknown", "gsm.sim.state": "LOADED,ABSENT",
                      "http.agent": "", "http.proxy": "", "net.dns1": "", "net.eth0.gw": "",
                      "net.gprs.local-ip": "", "net.hostname": "", "persist.sys.country": "",
                      "persist.sys.language": "", "ro.boot.hardware": "mt6833", "ro.boot.serialno": "",
                      "ro.build.date.utc": "1659417778", "ro.build.tags": "release-keys",
                      "ro.debuggable": "0", "ro.product.device": "evergo", "ro.serialno": "",
                      "sys.usb.state": "mtp,adb"}, "rc_app_code": "0000000000", "root": True,
            "screen": "1080,2260,440", "sdkver": "0.2.4",
            "sensor": "[\"Elliptic Proximity,Elliptic Labs\", \"ICM4N607 ACCELEROMETER,icm4n607_acc\", \"QMC6308 MAGNETOMETER,qmc6308\", \"ORIENTATION,MTK\", \"ICM4N607 GYROSCOPE,icm4n607_gyro\", \"TSL2522 LIGHT,TSL2522\", \"GRAVITY,MTK\", \"LINEARACCEL,MTK\", \"ROTATION_VECTOR,MTK\", \"UNCALI_MAG,MTK\", \"GAME_ROTATION_VECTOR,MTK\", \"UNCALI_GYRO,MTK\", \"SIGNIFICANT_MOTION,MTK\", \"STEP_DETECTOR,MTK\", \"STEP_COUNTER,MTK\", \"GEOMAGNETIC_ROTATION_VECTOR,MTK\", \"TILT_DETECTOR,MTK\", \"pickup  Wakeup,xiaomi\", \"DEVICE_ORIENTATION,MTK\", \"UNCALI_ACC,MTK\", \"STEP_DETECTOR_WAKEUP,MTK\", \"Touch Sensor,Xiaomi Large Area Detect\"]",
            "sensors_info": "[{\"name\":\"Elliptic Proximity\",\"vendor\":\"Elliptic Labs\",\"version\":\"4\",\"type\":\"8\",\"maxRange\":\"5.0\",\"resolution\":\"1.0E-4\",\"power\":\"0.5\",\"minDelay\":\"0\"}, {\"name\":\"ICM4N607 ACCELEROMETER\",\"vendor\":\"icm4n607_acc\",\"version\":\"1\",\"type\":\"1\",\"maxRange\":\"78.453606\",\"resolution\":\"0.0012\",\"power\":\"0.001\",\"minDelay\":\"2500\"}, {\"name\":\"QMC6308 MAGNETOMETER\",\"vendor\":\"qmc6308\",\"version\":\"1\",\"type\":\"2\",\"maxRange\":\"4912.0503\",\"resolution\":\"0.15\",\"power\":\"0.001\",\"minDelay\":\"20000\"}, {\"name\":\"ORIENTATION\",\"vendor\":\"MTK\",\"version\":\"1\",\"type\":\"3\",\"maxRange\":\"360.0\",\"resolution\":\"0.00390625\",\"power\":\"0.001\",\"minDelay\":\"5000\"}, {\"name\":\"ICM4N607 GYROSCOPE\",\"vendor\":\"icm4n607_gyro\",\"version\":\"1\",\"type\":\"4\",\"maxRange\":\"34.9063\",\"resolution\":\"0.0011\",\"power\":\"0.001\",\"minDelay\":\"2500\"}, {\"name\":\"TSL2522 LIGHT\",\"vendor\":\"TSL2522\",\"version\":\"1\",\"type\":\"5\",\"maxRange\":\"65535.0\",\"resolution\":\"1.0\",\"power\":\"0.001\",\"minDelay\":\"0\"}, {\"name\":\"GRAVITY\",\"vendor\":\"MTK\",\"version\":\"1\",\"type\":\"9\",\"maxRange\":\"39.226803\",\"resolution\":\"0.0012\",\"power\":\"0.001\",\"minDelay\":\"5000\"}, {\"name\":\"LINEARACCEL\",\"vendor\":\"MTK\",\"version\":\"1\",\"type\":\"10\",\"maxRange\":\"39.226803\",\"resolution\":\"0.0012\",\"power\":\"0.001\",\"minDelay\":\"5000\"}, {\"name\":\"ROTATION_VECTOR\",\"vendor\":\"MTK\",\"version\":\"1\",\"type\":\"11\",\"maxRange\":\"1.0\",\"resolution\":\"5.9604645E-8\",\"power\":\"0.001\",\"minDelay\":\"5000\"}, {\"name\":\"UNCALI_MAG\",\"vendor\":\"MTK\",\"version\":\"1\",\"type\":\"14\",\"maxRange\":\"4912.0503\",\"resolution\":\"0.15\",\"power\":\"0.001\",\"minDelay\":\"20000\"}, {\"name\":\"GAME_ROTATION_VECTOR\",\"vendor\":\"MTK\",\"version\":\"1\",\"type\":\"15\",\"maxRange\":\"1.0\",\"resolution\":\"5.9604645E-8\",\"power\":\"0.001\",\"minDelay\":\"5000\"}, {\"name\":\"UNCALI_GYRO\",\"vendor\":\"MTK\",\"version\":\"1\",\"type\":\"16\",\"maxRange\":\"34.9063\",\"resolution\":\"0.0011\",\"power\":\"0.001\",\"minDelay\":\"2500\"}, {\"name\":\"SIGNIFICANT_MOTION\",\"vendor\":\"MTK\",\"version\":\"1\",\"type\":\"17\",\"maxRange\":\"1.0\",\"resolution\":\"1.0\",\"power\":\"0.001\",\"minDelay\":\"-1\"}, {\"name\":\"STEP_DETECTOR\",\"vendor\":\"MTK\",\"version\":\"1\",\"type\":\"18\",\"maxRange\":\"1.0\",\"resolution\":\"1.0\",\"power\":\"0.001\",\"minDelay\":\"0\"}, {\"name\":\"STEP_COUNTER\",\"vendor\":\"MTK\",\"version\":\"1\",\"type\":\"19\",\"maxRange\":\"2.14748365E9\",\"resolution\":\"1.0\",\"power\":\"0.001\",\"minDelay\":\"0\"}, {\"name\":\"GEOMAGNETIC_ROTATION_VECTOR\",\"vendor\":\"MTK\",\"version\":\"1\",\"type\":\"20\",\"maxRange\":\"1.0\",\"resolution\":\"5.9604645E-8\",\"power\":\"0.001\",\"minDelay\":\"5000\"}, {\"name\":\"TILT_DETECTOR\",\"vendor\":\"MTK\",\"version\":\"1\",\"type\":\"22\",\"maxRange\":\"1.0\",\"resolution\":\"1.0\",\"power\":\"0.001\",\"minDelay\":\"0\"}, {\"name\":\"pickup  Wakeup\",\"vendor\":\"xiaomi\",\"version\":\"1\",\"type\":\"33171036\",\"maxRange\":\"1.0\",\"resolution\":\"1.0\",\"power\":\"0.001\",\"minDelay\":\"-1\"}, {\"name\":\"DEVICE_ORIENTATION\",\"vendor\":\"MTK\",\"version\":\"1\",\"type\":\"27\",\"maxRange\":\"3.0\",\"resolution\":\"1.0\",\"power\":\"0.001\",\"minDelay\":\"0\"}, {\"name\":\"UNCALI_ACC\",\"vendor\":\"MTK\",\"version\":\"1\",\"type\":\"35\",\"maxRange\":\"39.226803\",\"resolution\":\"0.0012\",\"power\":\"0.001\",\"minDelay\":\"2500\"}, {\"name\":\"STEP_DETECTOR_WAKEUP\",\"vendor\":\"MTK\",\"version\":\"1\",\"type\":\"18\",\"maxRange\":\"1.0\",\"resolution\":\"1.0\",\"power\":\"0.001\",\"minDelay\":\"0\"}, {\"name\":\"Touch Sensor\",\"vendor\":\"Xiaomi Large Area Detect\",\"version\":\"1\",\"type\":\"33171031\",\"maxRange\":\"5.0\",\"resolution\":\"1.0\",\"power\":\"1.0\",\"minDelay\":\"20\"}]",
            "sim": "5", "speed_sensor": "1", "ssid": "<unknown ssid>", "str_app_id": "1",
            "str_battery": "100", "str_brightness": "427",
            "sys": {"cpu_abi": "armeabi-v7a", "cpu_abi2": "armeabi", "device": "evergo",
                    "display": "evergo-user 12 SP1A.210812.016 V13.0.6.0.SGBCNXM",
                    "fingerprint": "Redmi/evergo/evergo:12/SP1A.210812.016/V13.0.6.0.SGBCNXM:user/release-keys",
                    "hardware": "mt6833", "manufacturer": "Xiaomi", "product": "evergo",
                    "serial": "unknown"}, "systemvolume": 10,
            "t": str(int(time.time() * 1000)),
            "totalSpace": 242948734976, "udid": "54f6ab6877163109", "ui_version": "V13.0.6.0.SGBCNXM",
            "uid": "10283", "usb_connected": "1", "vaid": "", "virtual": "0", "virtualproc": "[]",
            "voice_network_type": "0", "wifimac": self.wifi_mac, "wifimaclist": []
        }

        data_string = json.dumps(fingerprint_dict, separators=(",", ":"))
        random_string = self.create_random_string()

        device_meta = self.aes_encrypt(data_string, random_string, random_string)
        dt = self.rsa_encrypt(random_string)

        body = {
            'appkey': "bca7e84c2d947ac6",
            "bili_local_id": self.fp_local,
            'build': '6240300',
            'buvid': self.buvid,
            "c_locale": "zh_CN",
            'captcha_key': self.captcha_key,
            "channel": "xxl_gdt_wm_253",
            "cid": region,
            "code": code,
            "device": 'phone',
            'device_id': self.fp_remote,
            'device_meta': device_meta,
            'device_name': quote('Xiaomi21091116AC'),
            'device_platform': quote('Android12Xiaomi21091116AC'),
            'dt': quote_plus(dt),
            "from_pv": "main.homepage.avatar-nologin.all.click",
            "from_url": quote_plus("bilibili://user_center/mine"),
            "local_id": self.buvid,
            "mobi_app": "android",
            "platform": "android",
            "s_locale": "zh_CN",
            "tel": mobile,
            "ts": int(time.time()),
        }
        body_string = self.get_param_sign_so(body)

        if self.is_new:
            url = "https://passport.bilibili.com/x/passport-user/reg/sms"
            print("注册", end=">>>")
        else:
            url = "https://passport.bilibili.com/x/passport-login/login/sms"
            print("登录", end=">>>")

        resp = self.session.post(
            url=url,
            data=body_string.encode('utf-8'),
            headers={
                "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/MI 6 Plus mobi_app/android build/6240300 channel/xxl_gdt_wm_253 innerVer/6240300 osVer/6.0.1 network/2",
                'app-key': 'android',
                'env': 'prod',
                'buvid': self.buvid,
                "content-type": "application/x-www-form-urlencoded; charset=utf-8"
            }
        )

        data_dict = resp.json()
        print(data_dict)

        if self.is_new:
            # {'code': 0, 'message': '0', 'ttl': 1, 'data': {'mid': 1601198793, 'code': 'c70c21d614e79bd16b465fec24fc9781', 'hint': '注册成功', 'in_reg_audit': 0}}
            # 后面还要再登录
            self.mid = data_dict["data"]["mid"]
            self.code = data_dict["data"]["code"]
        else:
            # {'code': 0, 'message': '0', 'ttl': 1, 'data': {'status': 0, 'message': '', 'url': '', 'token_info': {'mid': 1601198793, 'access_token': 'd59c823cbf8c6c8b83e38a024c544c81', 'refresh_token': '5a50cb05c49673aecd04cf1d70291c81', 'expires_in': 15552000}, 'cookie_info': {'cookies': [{'name': 'SESSDATA', 'value': '7cb9740a%2C1676141339%2Cd892ac81', 'http_only': 1, 'expires': 1668365339, 'secure': 0}, {'name': 'bili_jct', 'value': '424c567ea5234f04ab82f825b08a6314', 'http_only': 0, 'expires': 1668365339, 'secure': 0}, {'name': 'DedeUserID', 'value': '1601198793', 'http_only': 0, 'expires': 1668365339, 'secure': 0}, {'name': 'DedeUserID__ckMd5', 'value': '56163e179dacd93c', 'http_only': 0, 'expires': 1668365339, 'secure': 0}, {'name': 'sid', 'value': '5prhj8q6', 'http_only': 0, 'expires': 1668365339, 'secure': 0}], 'domains': ['.bilibili.com', '.biligame.com', '.bigfun.cn', '.bigfunapp.cn', '.dreamcast.hk', '.bilibili.cn', '.shanghaihuanli.com']}, 'sso': ['https://passport.bilibili.com/api/v2/sso', 'https://passport.biligame.com/api/v2/sso', 'https://passport.bigfunapp.cn/api/v2/sso', 'https://passport.bilibili.cn/api/v2/sso', 'https://passport.shanghaihuanli.com/api/v2/sso']}}
            # 后面进行操作时需要带上cookie
            self.token_info = data_dict["data"]["token_info"]
            self.cookie_info = data_dict["data"]["cookie_info"]

    def step_oauth_access_token(self):
        body = {
            "appkey": "bca7e84c2d947ac6",
            "bili_local_id": self.fp_local,
            "build": "6240300",
            "buvid": self.buvid,
            "c_locale": "zh_CN",
            "channel": "xxl_gdt_wm_253",
            "code": self.code,
            "device": "phone",
            "device_id": self.fp_remote,
            "device_name": "XiaomiMI%206%20Plus",
            "device_platform": "Android6.0.1XiaomiMI%206%20Plus",
            "grant_type": "authorization_code",
            "local_id": self.buvid,
            "mobi_app": "android",
            "platform": "android",
            "s_locale": "zh_CN",
            "ts": str(int(time.time())),
        }

        body_string = self.get_param_sign_so(body)

        resp = self.session.post(
            url="https://passport.bilibili.com/x/passport-login/oauth2/access_token",
            data=body_string.encode('utf-8'),
            headers={
                "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/MI 6 Plus mobi_app/android build/6240300 channel/xxl_gdt_wm_253 innerVer/6240300 osVer/6.0.1 network/2",
                'app-key': 'android',
                'env': 'prod',
                'buvid': self.buvid,
                "content-type": "application/x-www-form-urlencoded; charset=utf-8"
            }
        )

        data_dict = resp.json()
        print("新设备登录返回值=>", data_dict)
        # {'code': 0, 'message': '0', 'ttl': 1, 'data': {'status': 0, 'message': '', 'url': '', 'token_info': {'mid': 2063928524, 'access_token': 'f422dd332b4106e4829f20d16efcde81', 'refresh_token': '7c7f34ca9ecbcb70040abc160fcffd81', 'expires_in': 15552000}, 'cookie_info': {'cookies': [{'name': 'SESSDATA', 'value': 'c0a7716f%2C1676141627%2Cb19f9881', 'http_only': 1, 'expires': 1668365627, 'secure': 0}, {'name': 'bili_jct', 'value': 'dd5aed78ef6934d562d43c061e9483e0', 'http_only': 0, 'expires': 1668365627, 'secure': 0}, {'name': 'DedeUserID', 'value': '2063928524', 'http_only': 0, 'expires': 1668365627, 'secure': 0}, {'name': 'DedeUserID__ckMd5', 'value': 'f99ed31d9511233d', 'http_only': 0, 'expires': 1668365627, 'secure': 0}, {'name': 'sid', 'value': '8488gk93', 'http_only': 0, 'expires': 1668365627, 'secure': 0}], 'domains': ['.bilibili.com', '.biligame.com', '.bigfun.cn', '.bigfunapp.cn', '.dreamcast.hk', '.bilibili.cn', '.shanghaihuanli.com']}, 'sso': ['https://passport.bilibili.com/api/v2/sso', 'https://passport.biligame.com/api/v2/sso', 'https://passport.bigfunapp.cn/api/v2/sso', 'https://passport.bilibili.cn/api/v2/sso', 'https://passport.shanghaihuanli.com/api/v2/sso']}}
        self.token_info = data_dict['data']['token_info']
        self.cookie_info = data_dict['data']['cookie_info']

    def get_card_fetch_code(self, card_url):
        for i in range(10):
            time.sleep(5)
            # {"flag":true,"data":[],"message":"[bilibili]验证码125772，5分钟内有效，请勿泄漏"}
            # {"flag":false,"data":[],"message":"No has message"}
            # 2022/09/12 22:04:18|[bilibili]验证码940574，5分钟内有效，请勿泄漏
            resp = requests.get(card_url)
            match_list = re.findall(r"\d{6}", resp.text)
            if not match_list:
                continue
            return str(match_list[0])


def run():
    card_dict = {
        "7828099329": "http://172.83.153.188/ussms?token=87b1882a493a084ea3a2a250b60fd5f1",
        "5813346981": "http://172.83.153.188/ussms?token=f58a1494638b5a36d3f11a6e49b73f4a",
        "5813316258": "http://172.83.153.188/ussms?token=a22b33e967c5d38f7f98a433d93e22b6",
        "2269013708": "http://172.83.153.188/ussms?token=bae57ae5f97c31cb567841fcf1563a01",
        "7828099414": "http://172.83.153.188/ussms?token=769216cd42bff50d9a2f5a978d99bbf8",
        "4037132861": "http://172.83.153.188/ussms?token=f08af8ea2e14dbec9da012cb84c760e2",
        "5813346141": "http://172.83.153.188/ussms?token=29aab81b086df9f7db14479fa6e7290c",
        "2269013506": "http://172.83.153.188/ussms?token=7249ebf7ec4836106812306cc4e9942e",
        "2269023228": "http://172.83.153.188/ussms?token=9bee343bdc96b38dd60346a56fa74032",
        "7828099172": "http://172.83.153.188/ussms?token=b9336ee4c9bd82a3ba4e8f1dc693589c"
    }

    region = "1"
    mobile = "5813346141"

    bili = Bilibili()

    # 获取公钥
    bili.step_web_key()

    # 注册设备，拿到guest_id
    bili.step_passport_guest_reg_5()

    # 发送短信
    need_geetest, gee_dict = bili.step_send_sms(region, mobile)
    print("正常发送短信=>", gee_dict)

    if gee_dict.get("code") == 86200:
        print(gee_dict["message"])  # 操作频繁
        return

    if need_geetest:
        gee_challenge = gee_dict["gee_challenge"]
        recaptcha_token = gee_dict["recaptcha_token"]

        gee_res_dict, gee_challenge = do_geetest(gee_challenge, gee_dict["gee_gt"], bili.get_proxy_dict())

        print("极验-验证=>", gee_res_dict, gee_challenge)

        gee_validate = gee_res_dict['validate']

        # 还需要再次发送短信
        status = bili.step_send_sms_geetest(region, mobile, gee_challenge, gee_validate, recaptcha_token)
        print(status)

    # 重新获取hash值
    bili.step_web_key()

    # 获取卡商验证码
    sms_code = bili.get_card_fetch_code(card_dict[mobile])
    print("验证码=>", sms_code)
    # sms_code = input(">>>")

    bili.step_login_sms(region, sms_code, mobile)
    if bili.is_new:
        bili.step_oauth_access_token()


if __name__ == '__main__':
    run()
    # print(int(time.time()))
