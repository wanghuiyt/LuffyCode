from hashlib import md5


def md5_encrypt(data_string):
    obj = md5()
    obj.update(data_string.encode("utf-8"))
    return obj.hexdigest()


security = "W@oCIAH_6Ew1f6%8"

data_dict = {
    "_appid": "atc.android",
    "appversion": "2.8.5",
    "channelid": "csy",
    "pwd": "e10adc3949ba59abbe56e057f20f883e",
    "udid": "ku6ieZi6gfDwXE6/0pZ29KylbBYZ2fTaY8T2Q0mz3BgRI8wojYRRH7rOtYB94h9uPFoYAm8CbXM=",
    "username": "18688999988"
}

result = "".join([f"{key}{data_dict[key]}" for key in sorted(data_dict.keys())])
un_sign_string = f"{security}{result}{security}"
sign = md5_encrypt(un_sign_string).upper()
print(sign)
