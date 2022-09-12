import uuid
import random
from hashlib import md5


def create_random_mac(sep=":"):
    """随机生成Mac地址"""
    data_list = []
    for i in range(1, 7):
        part = "".join(random.sample("0123456789ABCDEF", 2))
        data_list.append(part)
    mac = sep.join(data_list)
    return mac


def md5_encrypt(data_string):
    obj = md5()
    obj.update(data_string.encode("utf-8"))
    return obj.hexdigest()


def get_buvid_by_wifi_mac():
    mac = create_random_mac()
    v0_1 = md5_encrypt(mac)
    return f"XY{v0_1[2]}{v0_1[12]}{v0_1[22]}{v0_1}".upper()


def get_buvid_by_uuid():
    uuid_str = str(uuid.uuid4()).replace("-", "")
    return f"XW{uuid_str[2]}{uuid_str[12]}{uuid_str[22]}{uuid_str}".upper()


if __name__ == '__main__':
    # XY 开头
    buvid1 = get_buvid_by_wifi_mac()
    print(buvid1)
    # XW 开头
    buvid2 = get_buvid_by_uuid()
    print(buvid2)

