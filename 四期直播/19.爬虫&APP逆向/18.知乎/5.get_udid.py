import hmac
import random
import time
from hashlib import sha1
from urllib.parse import quote_plus

import requests


def get_random_mac(sep=":"):
    data_list = []
    for _ in range(1, 7):
        part = "".join(random.sample("0123456789ABCDEF", 2))
        data_list.append(part)
    return sep.join(data_list)


def get_signature(app_id, sign_version, data_string, ctime):
    key = "dd49a835-56e7-4a0f-95b5-efd51ea5397f"
    param_string = f"{app_id}{sign_version}{data_string}{ctime}"
    obj = hmac.new(key.encode("utf-8"), param_string.encode("utf-8"), sha1)
    return obj.hexdigest()


def get_udid():
    app_id = "1355"
    sign_version = "2"
    mac_str = get_random_mac()
    ctime = str(int(time.time()))
    mac_str = quote_plus(mac_str)
    data_string = f"app_build=1031&app_version=5.32.1&bt_ck=1&bundle_id=com.zhihu.android&cp_ct=8&cp_fq=2000000&cp_tp=0&cp_us=100.0&d_n=Android%20Bluedroid&fr_mem=463&fr_st=211620&latitude=0.0&longitude=0.0&mc_ad={mac_str}&mcc=cn&nt_st=1&ph_br=Redmi&ph_md=21091116AC&ph_os=Android%2012&ph_sn=unknown&pvd_nm=%E5%B0%8F%E7%B1%B3%E7%A7%BB%E5%8A%A8&tt_mem=512&tt_st=231693&tz_of=28800"
    signature = get_signature(app_id, sign_version, data_string, ctime)
    resp = requests.post(
        url="https://appcloud.zhihu.com/v1/device",
        data=data_string,
        headers={
            "x-req-signature": signature,
            "x-req-ts": ctime,
            "x-app-id": app_id,
            "x-sign-version": sign_version,
            "Host": "appcloud.zhihu.com",
            "User-Agent": "com.zhihu.android/Futureve/5.32.1 Mozilla/5.0 (Linux; Android 12; 21091116AC Build/SP1A.210812.016; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/99.0.4844.88 Mobile Safari/537.36",
        }
    )

    print(resp.json())
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
    print(resp.json())


if __name__ == '__main__':
    udid = get_udid()
    get_hd(udid)
