from hashlib import md5

obj = md5()
obj.update("123456".encode("utf-8"))
pwd = obj.hexdigest()
print(pwd)

token = ""
reqTime = "1661724890282"
nonce_str = "123456"
nonce_str_sub_2 = nonce_str[2:]
body_str = f"phone=18338725230&password={pwd}"
encrypt_str = f"{token}{reqTime}{nonce_str_sub_2}{body_str}"

obj = md5()
obj.update(encrypt_str.encode("utf-8"))
sign = obj.hexdigest()
print(sign)

