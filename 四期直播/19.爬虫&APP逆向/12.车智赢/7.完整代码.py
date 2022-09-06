import uuid
import random
import base64
import requests
from hashlib import md5
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad


def des3(data_string):
    # BS = 8
    # pad: Callable[[Any], Any] = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    # plaintext = pad(data_string).encode("utf-8")

    # 3DES的MODE_CBC模式下只有前24位有意义
    key = b'appapiche168comappapiche168comap'[0:24]
    iv = b'appapich'
    plaintext = pad(data_string.encode("utf-8"), 8)

    # 使用MODE_CBC创建cipher
    cipher = DES3.new(key=key, mode=DES3.MODE_CBC, IV=iv)
    result = cipher.encrypt(plaintext)
    return base64.b64encode(result).decode("utf-8")


def md5_encrypt(data_string):
    obj = md5()
    obj.update(data_string.encode("utf-8"))
    return obj.hexdigest()


def run():
    username = "13146372546"
    password = "123456"

    imei = str(uuid.uuid4())
    nano_time = random.randint(4191649692556, 7136066335773)
    device_id = ""
    udid = des3(f"{imei}|{nano_time}|{device_id}")

    security = "W@oC!AH_6Ew1f6%8"

    data_dict = {
        "_appid": "atc.android",
        "appversion": "2.8.5",
        "channelid": "csy",
        "pwd": md5_encrypt(password),
        "udid": udid,
        "username": username
    }

    result = "".join([f"{key}{data_dict[key]}" for key in sorted(data_dict.keys())])
    un_sign_string = f"{security}{result}{security}"
    sign = md5_encrypt(un_sign_string).upper()
    data_dict["_sign"] = sign

    resp = requests.post(
        url="https://dealercloudapi.che168.com/tradercloud/sealed/login/login.ashx",
        data=data_dict
    )
    print(resp.text)


if __name__ == '__main__':
    run()
