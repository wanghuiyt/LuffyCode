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

    def step_web_key(self):
        param_dict = {
            "appkey": "1d8b6e7d45233436",
            "build": "6240300",
            "c_locale": "zh_CN",
            "channel": "xxl_gdt_wm_253",
            "mobi_app": "android",
            "platform": "android",
            "s_locale": "zh_CN",
            "statistics": "%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%226.24.0%22%2C%22abtest%22%3A%22%22%7D",
            "ts": int(time.time()),
        }
        sign_param_string = self.get_param_sign_so(param_dict)
        res = self.session.get(
            url="https://passport.bilibili.com/x/passport-login/web/key?{}".format(sign_param_string),
            headers={
                "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/MI 6 Plus mobi_app/android build/6240300 channel/xxl_gdt_wm_253 innerVer/6240300 osVer/6.0.1 network/2",
                "buvid": self.buvid,
                'env': "prod",
                'app-key': "android",
                "content-type": "application/x-www-form-urlencoded; charset=utf-8"
            }
        )
        data_dict = res.json()
        print("4.获取秘钥", data_dict)

        self.hash = data_dict['data']['hash']
        self.rsa_pub_key = data_dict['data']['key']

    def get_random_string(self, count=16):
        ca = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        char_list = []
        for v2 in range(count):
            char = random.choice(ca)
            char_list.append(char)
        return "".join(char_list)

    def aes_encrypt_to_hex_string(self, data, key, iv):
        aes = AES.new(
            key=key.encode('utf-8'),
            mode=AES.MODE_CBC,
            iv=iv.encode('utf-8')
        )
        raw = pad(data.encode('utf-8'), 16)
        encrypt_bytes = aes.encrypt(raw)
        hex_string = ''.join(['%02X' % b for b in encrypt_bytes])
        return hex_string

    def rsa_encrypt_v2(self, s):
        """校验RSA加密 使用公钥进行加密"""
        key = RSA.importKey(self.rsa_pub_key)
        cipher = PKCS1_v1_5.new(key)
        ciphertext = b64encode(cipher.encrypt(bytes(s, "utf-8")))
        return ciphertext

    def step_login_sms(self, region, code, mobile):
        fingerprint_dict = {
            "aaid": "",
            "accessibility_service": "[\"com.ss.android.ugc.aweme/.live.livehostimpl.AudioAccessibilityService\"]",
            "adb_enabled": "1", "adid": "23cbedaf5331524f",
            "androidapp20": "[\"1660031213405,com.che168.autotradercloud,0,2.8.2,243,1660031213405\", \"1652360056481,com.nb.liyang,0,1.0,1,1652360056481\", \"1654267588502,com.rt.market.fresh,0,1.6.7,1067000,1654267588502\", \"1654268270117,cn.rainbow.westore,0,5.0.0,5000,1654268270117\", \"1643116515115,com.yltx.oil.partner,0,1.4,5,1643116515115\", \"1646723015695,com.shizhuang.duapp,0,4.97.1,511,1659012101546\", \"1646727783087,org.sandroproxy.drony,0,1.3.102,102,1646727783087\", \"1645088871314,com.ss.android.ugc.aweme,0,15.4.0,150401,1645088871314\", \"1646308560781,com.net.weishibao.redirect.resolverD.interface4,0,1.7.6,75,1646308560781\", \"1648118226760,com.zhihu.android,0,5.32.1,1031,1648118226760\", \"1654336862909,com.feng.car,0,4.3.2.6,187,1654336862909\", \"1645089047912,com.netease.open.pocoservice,0,1.0.0.43,43,1645089047912\", \"1643113901585,hyz.pm.tibet.preparation.android.uat,0,1.0.16,702,1650977541746\", \"1646911960716,tv.danmaku.bili,0,6.24.0,6240300,1646911960716\", \"1645263708606,com.iqilu.app137,0,0.0.28,108,1645263708606\"]",
            "androidappcnt": 71,
            "androidsysapp20": "[\"1631951462000,com.android.providers.telephony,1,6.0.1,23,1631951462000\", \"1631951449000,com.android.providers.calendar,1,6.0.1,23,1631951449000\", \"1631951305000,com.netease.nemu_vinput.nemu,1,2.1.2,212,1631951305000\", \"1631951450000,com.android.providers.media,1,6.0.1,800,1631951450000\", \"1631951501000,com.android.wallpapercropper,1,6.0.1,23,1631951501000\", \"1631951502000,com.android.documentsui,1,6.0.1,23,1631951502000\", \"1631951299000,com.android.galaxy4,1,1.0,1,1631951299000\", \"1631951449000,com.android.externalstorage,1,6.0.1,23,1631951449000\", \"1631951450000,com.android.htmlviewer,1,6.0.1,23,1631951450000\", \"1631951452000,com.android.quicksearchbox,1,6.0.1,23,1631951452000\", \"1631951458000,com.android.mms.service,1,6.0.1,23,1631951458000\", \"1631951449000,com.android.providers.downloads,1,6.0.1,23,1631951449000\", \"1631951514000,com.android.browser,1,6.0.1,23,1631951514000\", \"1631951449000,com.android.defcontainer,1,6.0.1,23,1631951449000\", \"1631951450000,com.android.providers.downloads.ui,1,6.0.1,23,1631951450000\", \"1631951450000,com.android.pacprocessor,1,6.0.1,23,1631951450000\", \"1631951450000,com.android.certinstaller,1,6.0.1,23,1631951450000\", \"1631951353000,android,1,6.0.1,23,1631951353000\", \"1631951531000,com.android.contacts,1,6.0.1,23,1631951531000\", \"1631951538000,com.android.camera2,1,2.0.002 (eng.duanlusheng.114c31b0b.091821_154805-00),20002000,1631951538000\"]",
            "app_id": "1", "app_version": "6.24.0", "app_version_code": "6240300",
            "apps": "[\"1631951462000,com.android.providers.telephony,1,6.0.1,23,1631951462000\",\"1660031213405,com.che168.autotradercloud,0,2.8.2,243,1660031213405\",\"1631951449000,com.android.providers.calendar,1,6.0.1,23,1631951449000\",\"1631951305000,com.netease.nemu_vinput.nemu,1,2.1.2,212,1631951305000\",\"1631951450000,com.android.providers.media,1,6.0.1,800,1631951450000\",\"1631951501000,com.android.wallpapercropper,1,6.0.1,23,1631951501000\",\"1652360056481,com.nb.liyang,0,1.0,1,1652360056481\",\"1654267588502,com.rt.market.fresh,0,1.6.7,1067000,1654267588502\",\"1631951502000,com.android.documentsui,1,6.0.1,23,1631951502000\",\"1631951299000,com.android.galaxy4,1,1.0,1,1631951299000\",\"1631951449000,com.android.externalstorage,1,6.0.1,23,1631951449000\",\"1631951450000,com.android.htmlviewer,1,6.0.1,23,1631951450000\",\"1631951452000,com.android.quicksearchbox,1,6.0.1,23,1631951452000\",\"1631951458000,com.android.mms.service,1,6.0.1,23,1631951458000\",\"1631951449000,com.android.providers.downloads,1,6.0.1,23,1631951449000\",\"1631951514000,com.android.browser,1,6.0.1,23,1631951514000\",\"1654268270117,cn.rainbow.westore,0,5.0.0,5000,1654268270117\",\"1631951449000,com.android.defcontainer,1,6.0.1,23,1631951449000\",\"1631951450000,com.android.providers.downloads.ui,1,6.0.1,23,1631951450000\",\"1631951450000,com.android.pacprocessor,1,6.0.1,23,1631951450000\"]",
            "axposed": "false", "band": "j8LhNc", "battery": 79, "batteryState": "",
            "biometric": "0",
            "biometrics": "", "boot": "14952961", "brand": "Xiaomi", "brightness": "102",
            "bssid": "6a:38:4c:68:4e:63", "btmac": "", "build_id": "V417IR release-keys",
            'buvid_local': self.buvid,
            "chid": "xxl_gdt_wm_253", "countryIso": "",
            "cpuCount": "2", "cpuFreq": "2400000", "cpuModel": "", "cpuVendor": "Qualcomm",
            "data_activity_state": "0", "data_connect_state": "0",
            "device_angle": "-1.5707964,3.1415927,-0.0",
            "emu": "100", "files": "/data/user/0/tv.danmaku.bili/files", "first": "false",
            "free_memory": "3457769472", "fstorage": 130199601152,
            'fts': self.app_first_run_time,
            "gadid": "", "glimit": "",
            "gps_sensor": "1",
            'guest_id': self.guest_id,
            "guid": "2973199f-cd83-431f-bdf4-c8c98f967c52",
            "gyroscope_sensor": "1", "is_root": "true", "kernel_version": "4.0.9-android-x86_64+",
            "languages": "zh",
            'last_dump_ts': str(int(time.time() * 1000)),
            "light_intensity": "350.0",
            "linear_speed_sensor": "1",
            'mac': self.wifi_mac,
            "maps": "", "mem": "4145094656",
            "memory": "4145094656", "mid": "", "model": "MI 6 Plus",
            "net": "[\"lo,::1%1,127.0.0.1,\", \"wlan0,fe80::a00:27ff:fef1:5e03%wlan0,10.0.2.15,{}\"]".format(
                self.wifi_mac),
            "network": "WIFI", "oaid": "", "oid": "", "os": "android", "osver": "6.0.1",
            "proc": "tv.danmaku.bili",
            "props": {"gsm.network.type": "", "gsm.sim.state": "", "http.agent": "",
                      "http.proxy": "",
                      "net.dns1": "192.168.0.1", "net.eth0.gw": "", "net.gprs.local-ip": "",
                      "net.hostname": "android-23cbedaf5331524f", "persist.sys.country": "",
                      "persist.sys.language": "", "ro.boot.hardware": "",
                      "ro.boot.serialno": "ZX1G42CPJD",
                      "ro.build.date.utc": "1631951299", "ro.build.tags": "release-keys",
                      "ro.debuggable": "1",
                      "ro.product.device": "x86_64", "ro.serialno": "ZX1G42CPJD",
                      "sys.usb.state": "none"},
            "rc_app_code": "0000000000", "root": True, "screen": "1170,1872,416",
            "sdkver": "0.2.4",
            "sensor": "[\"BML160 Accelerometer,BML160\", \"LSM330DLC Gyroscope sensor,MEMS\", \"BML160 Magnetometer,BML160\", \"BML160 Gravity,BML160\", \"LTR559 Ambient Light Sensor,LITE-ON TECHNOLOGY CORP.\", \"iNemoEngine Game Rotation Vector sensor,NemoEngine\", \"iNemoEngine Orientation sensor,STMicroelectronics\", \"BHI160 GeoMag Rotation Vector Sensor,BHI\", \"CM36651 Proximity sensor,Capella Microsystems, Inc\", \"Miran KPC-400mm Linear Acceleration,Miran\", \"BML160 Rotation Vector Sensor,BML\"]",
            "sensors_info": "[{\"name\":\"BML160 Accelerometer\",\"vendor\":\"BML160\",\"version\":\"1\",\"type\":\"1\",\"maxRange\":\"19.6133\",\"resolution\":\"0.009576807\",\"power\":\"0.57\",\"minDelay\":\"5000\"}, {\"name\":\"LSM330DLC Gyroscope sensor\",\"vendor\":\"MEMS\",\"version\":\"1\",\"type\":\"4\",\"maxRange\":\"0.0\",\"resolution\":\"0.0\",\"power\":\"0.0\",\"minDelay\":\"0\"}, {\"name\":\"BML160 Magnetometer\",\"vendor\":\"BML160\",\"version\":\"1\",\"type\":\"2\",\"maxRange\":\"0.0\",\"resolution\":\"0.0\",\"power\":\"0.0\",\"minDelay\":\"0\"}, {\"name\":\"BML160 Gravity\",\"vendor\":\"BML160\",\"version\":\"1\",\"type\":\"9\",\"maxRange\":\"0.0\",\"resolution\":\"0.0\",\"power\":\"0.0\",\"minDelay\":\"0\"}, {\"name\":\"LTR559 Ambient Light Sensor\",\"vendor\":\"LITE-ON TECHNOLOGY CORP.\",\"version\":\"1\",\"type\":\"5\",\"maxRange\":\"0.0\",\"resolution\":\"0.0\",\"power\":\"0.0\",\"minDelay\":\"0\"}, {\"name\":\"iNemoEngine Game Rotation Vector sensor\",\"vendor\":\"NemoEngine\",\"version\":\"1\",\"type\":\"15\",\"maxRange\":\"0.0\",\"resolution\":\"0.0\",\"power\":\"0.0\",\"minDelay\":\"0\"}, {\"name\":\"iNemoEngine Orientation sensor\",\"vendor\":\"STMicroelectronics\",\"version\":\"1\",\"type\":\"3\",\"maxRange\":\"0.0\",\"resolution\":\"0.0\",\"power\":\"0.0\",\"minDelay\":\"0\"}, {\"name\":\"BHI160 GeoMag Rotation Vector Sensor\",\"vendor\":\"BHI\",\"version\":\"1\",\"type\":\"20\",\"maxRange\":\"0.0\",\"resolution\":\"0.0\",\"power\":\"0.0\",\"minDelay\":\"0\"}, {\"name\":\"CM36651 Proximity sensor\",\"vendor\":\"Capella Microsystems, Inc\",\"version\":\"1\",\"type\":\"8\",\"maxRange\":\"0.0\",\"resolution\":\"0.0\",\"power\":\"0.0\",\"minDelay\":\"0\"}, {\"name\":\"Miran KPC-400mm Linear Acceleration\",\"vendor\":\"Miran\",\"version\":\"1\",\"type\":\"10\",\"maxRange\":\"0.0\",\"resolution\":\"0.0\",\"power\":\"0.0\",\"minDelay\":\"0\"}, {\"name\":\"BML160 Rotation Vector Sensor\",\"vendor\":\"BML\",\"version\":\"1\",\"type\":\"11\",\"maxRange\":\"0.0\",\"resolution\":\"0.0\",\"power\":\"0.0\",\"minDelay\":\"0\"}]",
            "sim": "0", "speed_sensor": "1", "ssid": "\"j8LhNc\"", "str_app_id": "1",
            "str_battery": "30",
            "str_brightness": "102",
            "sys": {"cpu_abi": "armeabi-v7a", "cpu_abi2": "armeabi", "device": "x86_64",
                    "display": "V417IR release-keys",
                    "fingerprint": "OnePlus/OnePlus2/OnePlus2:6.0.1/MMB29M/1447841200:user/release-keys",
                    "hardware": "cancro_x86_64", "manufacturer": "Xiaomi",
                    "product": "cancro_x86_64", "serial": "ZX1G42CPJD"}, "systemvolume": 5,
            't': str(int(time.time() * 1000)),
            "totalSpace": 135148310528, "udid": "23cbedaf5331524f",
            "ui_version": "eng.duanlusheng.20210918.154646", "uid": "10042", "vaid": "",
            "virtual": "0",
            "virtualproc": "[]",
            "wifimac": self.wifi_mac,
            "wifimaclist": []
        }

        data_string = json.dumps(fingerprint_dict, separators=(',', ':'))
        random_string = self.get_random_string(16)

        device_meta = self.aes_encrypt_to_hex_string(data_string, random_string, random_string)
        dt = self.rsa_encrypt_v2(random_string)

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
            'device_name': quote('XiaomiMI 6 Plus'),
            'device_platform': quote('Android6.0.1XiaomiMI 6 Plus'),
            'dt': quote_plus(dt),
            "from_pv": "main.homepage.avatar-nologin.all.click",
            "from_url": "bilibili%3A%2F%2Fpegasus%2Fpromo",
            "local_id": self.buvid,
            "mobi_app": "android",
            "platform": "android",
            "s_locale": "zh_CN",
            "tel": mobile,
            "ts": int(time.time()),
        }
        total_body_string = self.get_param_sign_so(body)

        if self.is_new:
            url = "https://passport.bilibili.com/x/passport-user/reg/sms"
        else:
            url = "https://passport.bilibili.com/x/passport-login/login/sms"

        res = self.session.post(
            url=url,
            data=total_body_string.encode('utf-8'),
            headers={
                # "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/Mate 10 Pro mobi_app/android build/6240300 channel/bili innerVer/6240300 osVer/6.0.1 network/2",
                "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/MI 6 Plus mobi_app/android build/6240300 channel/xxl_gdt_wm_253 innerVer/6240300 osVer/6.0.1 network/2",
                'app-key': 'android',
                'env': 'prod',
                'buvid': self.buvid,
                "content-type": "application/x-www-form-urlencoded; charset=utf-8"
            }
        )
        # 3.发送请求
        data_dict = res.json()
        print("登录：", data_dict)
        if self.is_new:
            # {'code': 0, 'message': '0', 'ttl': 1, 'data': {'mid': 1601198793, 'code': 'c70c21d614e79bd16b465fec24fc9781', 'hint': '注册成功', 'in_reg_audit': 0}}
            # 去登录
            self.mid = data_dict['data']['mid']
            self.code = data_dict['data']['code']
        else:
            # {'code': 0, 'message': '0', 'ttl': 1, 'data': {'status': 0, 'message': '', 'url': '', 'token_info': {'mid': 1601198793, 'access_token': 'd59c823cbf8c6c8b83e38a024c544c81', 'refresh_token': '5a50cb05c49673aecd04cf1d70291c81', 'expires_in': 15552000}, 'cookie_info': {'cookies': [{'name': 'SESSDATA', 'value': '7cb9740a%2C1676141339%2Cd892ac81', 'http_only': 1, 'expires': 1668365339, 'secure': 0}, {'name': 'bili_jct', 'value': '424c567ea5234f04ab82f825b08a6314', 'http_only': 0, 'expires': 1668365339, 'secure': 0}, {'name': 'DedeUserID', 'value': '1601198793', 'http_only': 0, 'expires': 1668365339, 'secure': 0}, {'name': 'DedeUserID__ckMd5', 'value': '56163e179dacd93c', 'http_only': 0, 'expires': 1668365339, 'secure': 0}, {'name': 'sid', 'value': '5prhj8q6', 'http_only': 0, 'expires': 1668365339, 'secure': 0}], 'domains': ['.bilibili.com', '.biligame.com', '.bigfun.cn', '.bigfunapp.cn', '.dreamcast.hk', '.bilibili.cn', '.shanghaihuanli.com']}, 'sso': ['https://passport.bilibili.com/api/v2/sso', 'https://passport.biligame.com/api/v2/sso', 'https://passport.bigfunapp.cn/api/v2/sso', 'https://passport.bilibili.cn/api/v2/sso', 'https://passport.shanghaihuanli.com/api/v2/sso']}}
            self.token_info = data_dict['data']['token_info']
            self.cookie_info = data_dict['data']['cookie_info']

    def step_passport_guest_reg_5(self):
        """ 游客注册，用于获取游客 GuestId """

        device_info_dict = {
            "AndroidID": self.android_id,
            "BuildBrand": self.build_brand,
            "BuildDisplay": self.build_display,
            "BuildFingerprint": self.build_fingerprint,
            "BuildHost": "a11-gz02-test.i.nease.net",
            "Buvid": self.buvid,
            "DeviceType": "Android",
            "MAC": self.wifi_mac,
            "fts": self.app_first_run_time
        }

        # 1. 根据这个字典信息生成 dt 和 device_info（顺序不能乱）
        data_string = json.dumps(device_info_dict, separators=(',', ':'))
        random_string = self.get_random_string(16)

        device_info = self.aes_encrypt_to_hex_string(data_string, random_string, random_string)
        dt = self.rsa_encrypt_v2(random_string)

        # 2.构造参数，调用 so 文件进行签名

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
        total_body_string = self.get_param_sign_so(body)
        res = self.session.post(
            url="https://passport.bilibili.com/x/passport-user/guest/reg",
            data=total_body_string.encode('utf-8'),
            headers={
                "user-agent": "Mozilla/5.0 BiliDroid/6.24.0 (bbcallen@gmail.com) os/android model/Mate 10 Pro mobi_app/android build/6240300 channel/bili innerVer/6240300 osVer/6.0.1 network/2",
                'app-key': 'android',
                'env': 'prod',
                'buvid': self.buvid,
                "content-type": "application/x-www-form-urlencoded; charset=utf-8"
            }
        )
        # 3.发送请求
        data_dict = res.json()
        self.guest_id = str(data_dict['data']['guest_id'])


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
    mobile = "5813316258"
    proxy_dict = get_proxy_dict()
    bili = BiliBili(proxy_dict)

    # key+注册设备
    bili.step_web_key()
    bili.step_passport_guest_reg_5()

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

    bili.step_web_key()
    sms_code = input(">>>")
    bili.step_login_sms(region, sms_code, mobile)


if __name__ == '__main__':
    run()
