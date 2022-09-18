import hmac
import random
import time
from hashlib import sha1, md5
from urllib.parse import quote_plus

import execjs
import requests


def create_random_mac(sep=":"):
    """随机生成mac地址"""
    def mac_same_char(mac_str):
        v0 = mac_str[0]
        index = 1
        while index < len(mac_str):
            if v0 != mac_str[index]:
                return False
            index += 1
        return True

    data_list = []
    for i in range(1, 7):
        part = "".join(random.sample("0123456789ABCDEF", 2))
        data_list.append(part)
    mac = sep.join(data_list)
    if not mac_same_char(mac) and mac != "D4:3B:04:CE:6A:BC":
        return mac
    return create_random_mac(sep)


def encrypt_so(app_id, sign_version, ts, params_string):
    key = "dd49a835-56e7-4a0f-95b5-efd51ea5397f"
    data_string = f"{app_id}{sign_version}{params_string}{ts}"
    obj = hmac.new(key.encode("utf-8"), data_string.encode("utf-8"), sha1)
    return obj.hexdigest()


def get_udid():
    app_id = "1355"
    sign_version = "2"
    ts = str(int(time.time()))
    mac_str = create_random_mac()
    mac_quote_string = quote_plus(mac_str)
    form_string = f"app_build=1031&app_version=5.32.1&bt_ck=1&bundle_id=com.zhihu.android&cp_ct=8&cp_fq=2000000&cp_tp=0&cp_us=100.0&d_n=Android%20Bluedroid&fr_mem=461&fr_st=211570&latitude=0.0&longitude=0.0&mc_ad={mac_quote_string}&mcc=cn&nt_st=1&ph_br=Redmi&ph_md=21091116AC&ph_os=Android%2012&ph_sn=unknown&pvd_nm=%E5%B0%8F%E7%B1%B3%E7%A7%BB%E5%8A%A8&tt_mem=512&tt_st=231693&tz_of=28800"

    sign = encrypt_so(app_id, sign_version, ts, form_string)

    resp = requests.post(
        url="https://appcloud.zhihu.com/v1/device",
        data=form_string,
        headers={
            "x-req-signature": sign,
            "x-req-ts": ts,
            "x-app-id": app_id,
            "x-sign-version": sign_version,
            "Host": "appcloud.zhihu.com",
            "User-Agent": "com.zhihu.android/Futureve/5.32.1 Mozilla/5.0 (Linux; Android 12; 21091116AC Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/99.0.4844.88 Mobile Safari/537.36",
        }
    )
    return resp.json()["udid"]


def get_hd(udid):
    resp = requests.post(
        url="https://api.zhihu.com/guests/token",
        data={
            "source": "com.zhihu.android"
        },
        headers={
            "x-udid": udid,
            "x-app-version": "5.32.1",
            "User-Agent": "com.zhihu.android/Futureve/5.32.1 Mozilla/5.0 (Linux; Android 12; 21091116AC Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/99.0.4844.88 Mobile Safari/537.36",
        }
    )
    return resp.json()["id"]


def get_cookie_d_c0():
    resp = requests.get(
        url="https://www.zhihu.com",
        headers={
            "User-Agent": "com.zhihu.android/Futureve/5.32.1 Mozilla/5.0 (Linux; Android 12; 21091116AC Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/99.0.4844.88 Mobile Safari/537.36"
        }
    )
    return resp.cookies.get_dict()["d_c0"]


def md5_encrypt(data_string):
    obj = md5()
    obj.update(data_string.encode("utf-8"))
    return obj.hexdigest()


def encrypt(md5_str):
    with open("8.v1.js", mode="r", encoding="utf-8") as f:
        js = f.read()

    ct = execjs.compile(js).call("get_sign", md5_str)
    b = bytearray()
    # for i in ct:
    #     b.append(i)
    # print(b.decode("utf-8"))
    return ct


def get_zse_96(url_string):
    zse_93 = "101_3_3.0"
    d_c0 = get_cookie_d_c0()

    data_string = f"{zse_93}+{url_string}+{d_c0}"

    md5_str = md5_encrypt(data_string)

    # 调用execjs去进行加密处理
    part_sign = encrypt(md5_str)

    return f"2.0_{part_sign}"


def run():
    udid = get_udid()
    hd = get_hd(udid)

    url_string = "/api/v4/search_v3?gk_version=gz-gaokao&q=%E6%AD%A6%E6%B2%9B%E9%BD%90&t=general&lc_idx=0&correction=1&offset=0&advert_count=0&limit=20&is_real_time=0&show_all_topics=0&search_source=History&filter_fields=&city=&pin_flow=false&ruid=&recq=&raw_query="

    zse_96 = get_zse_96(url_string)

    resp = requests.get(
        url=f"https://www.zhihu.com{url_string}",
        headers={
            "x-udid": udid,
            "x-ac-udid": udid,
            "x-zse-96": zse_96,
            "x-hd": hd,
            "x-zse-93": "101_3_3.0",
            'x-app-version': "5.32.1",
            "User-Agent": "com.zhihu.android/Futureve/5.32.1 Mozilla/5.0 (Linux; Android 12; 21091116AC Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/99.0.4844.88 Mobile Safari/537.36"
        }
    )
    print(resp.text)


if __name__ == '__main__':
    run()
