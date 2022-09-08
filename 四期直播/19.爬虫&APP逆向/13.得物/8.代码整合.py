import json
import time
import copy
import random
import base64
import requests
from hashlib import md5
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def create_android_id(size=9):
    data_list = []
    for i in range(1, size):
        part = "".join(random.sample("0123456789ABCDEF", 2))
        data_list.append(part)
    return "".join(data_list).lower()


def md5_encrypt(data_bytes):
    obj = md5()
    obj.update(data_bytes)
    return obj.hexdigest()


def aes_encrypt(data_string):
    key = "d245a0ba8d678a61"
    aes = AES.new(
        key=key.encode("utf-8"),
        mode=AES.MODE_ECB
    )
    raw = pad(data_string.encode("utf-8"), 16)
    return aes.encrypt(raw)


def get_sign(data_dict):
    ordered_string = "".join(["{}{}".format(key, data_dict[key]) for key in sorted(data_dict.keys())])

    aes_string = aes_encrypt(ordered_string)
    aes_string = base64.encodebytes(aes_string)
    aes_string = aes_string.replace(b"\n", b"")
    sign = md5_encrypt(aes_string)
    return sign

def get_tunel_proxies():
    proxy_host = "tps150.kdlapi.com:15818"
    proxy_username = "t12678079599196"
    proxy_pwd = "gbtn0lkl"
    return {
        "http": "http://{}:{}@{}".format(proxy_username, proxy_pwd, proxy_host),
        "https": "https://{}:{}@{}".format(proxy_username, proxy_pwd, proxy_host)
    }


PROXIES = get_tunel_proxies()
uid = create_android_id()
ctime = str(int(time.time() * 1000))
param_dict = {
    "loginToken": "",
    "platform": "android",
    "timestamp": ctime,
    "uuid": uid,
    "v": "4.84.0"
}

param_dict["newSign"] = get_sign(param_dict)
param_dict.pop("uuid")
length = len(json.dumps(param_dict, separators=(',',':')))

resp = requests.post(
    url="https://app.dewu.com/api/v1/app/user_core/users/getVisitorUserId",
    # proxies=PROXIES,
    headers={
        "duuuid": uid,
        'duplatform': 'android',
        'appId': 'duapp',
        'duchannel': 'guagndiantong360',
        'humeChannel': '',
        'duv': '4.84.0',
        'duloginToken': '',
        'dudeviceTrait': '21091116AC',
        'dudeviceBrand': 'Redmi',
        'timestamp': ctime,
        'shumeiid': '20220908205718602e1ecde90ceae6a6fce3db2530b6ca00d38c42c939f105',
        'oaid': '',
        'User-Agent': 'duapp/4.84.0(android;12)',
        'X-Auth-Token': '',
        'isRoot': '0',
        'emu': '0',
        'isProxy': '0',
        'SK': '',
        'duimei': '',
        # 'duproductid': 'A9EE83DA6AFC9930AD4E087C922FA1C6BDFE24914A4EEF24D4D5C25559243BDD',
        'dps': '1',
        'Content-Type': 'application/json; charset=utf-8',
        'Host': 'app.dewu.com',
        'Accept-Encoding': 'gzip',
        'Content-Length': str(length),
        'Connection': 'keep-alive'
    },
    json=param_dict
)

x_auth_token = resp.headers["X-Auth-Token"]
print(x_auth_token)

reply_param_dict = {
    "contentId": "86602895",
    "contentType": "0",
    "anchorReplyId": "0",
    "lastId": "",
    "source": "",
    "limit": "20",
}

new_dict = copy.deepcopy(reply_param_dict)
new_dict.update({"loginToken": "", "platform": "android", "timestamp": str(int(time.time() * 1000)), "uuid": uid, "v": "4.84.0"})

reply_param_dict["newSign"] = get_sign(new_dict)
resp = requests.get(
    url="https://app.dewu.com/sns-itr/v1/reply/content-reply-list",
    params=reply_param_dict,
    headers={
        "X-Auth-Token": x_auth_token,
        "User-Agent": "duapp/4.84.0(android;12)"
    }
)
print(resp.text)
