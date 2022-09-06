import uuid
import random
import base64
from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad


def des3(data_string):
    # 3DES的MODE_CBC模式下只有前24位有意义
    key = b'appapiche168comappapiche168comap'[0:24]
    iv = b'appapich'
    plaintext = pad(data_string.encode("utf-8"), 8)

    # 使用MODE_CBC创建cipher
    cipher = DES3.new(key=key, mode=DES3.MODE_CBC, IV=iv)
    result = cipher.encrypt(plaintext)
    res = base64.b64encode(result).decode("utf-8")
    return res


def run():
    imei = str(uuid.uuid4())
    nano_time = random.randint(4191649692556, 4223970081789)
    device_id = ""  # 20 290001
    udid = des3(f"{imei}|{nano_time}|{device_id}")
    print(udid)


if __name__ == '__main__':
    run()
