import random
from hashlib import md5
from datetime import datetime


def gen_local_v1(buvid, phone_model, phone_band):
    """
    fp_local和fp_remote都是用这个算法来生成的，在手机初始化阶段生成fp_local
    :param buvid: 根据算法生成buvid，例如："XX8A435834E141A46A111E6DEDD4D97D68E09"
    :param phone_model: 手机型号，例如："2019xxxAC"
    :param phone_band: 手机品牌
    :return:
    """

    def misc_helper_kt(data_bytes):
        data_list = []
        v7 = len(data_bytes)
        v0 = 0
        while v0 < v7:
            v2 = data_bytes[v0]
            data_list.append("%02x" % v2)
            v0 += 1
        return "".join(data_list)

    data_string = f"{buvid}{phone_model}{phone_band}"
    obj = md5()
    obj.update(data_string.encode("utf-8"))
    data = obj.digest()
    arg1 = misc_helper_kt(data)
    arg2 = datetime.now().strftime("%Y%m%d%H%M%S")
    arg3 = misc_helper_kt([random.randint(0, 255) for i in range(8)])

    return f"{arg1}{arg2}{arg3}"


def a_b(arg8):
    v3 = 0
    v4 = 60
    v0_1 = 2
    v5 = 0
    while True:
        v6 = arg8[v3: v3 + 2]
        v5 += int(v6, base=16)
        if v3 != v4:
            v3 += v0_1
            continue
        break
    data = "%02x" % (v5 % 0x100, )
    return data


str2 = gen_local_v1("XX8A435834E141A46A111E6DEDD4D97D68E09", "2019xxxAC", "")
fp_local = str2 + a_b(str2)
print(fp_local)

