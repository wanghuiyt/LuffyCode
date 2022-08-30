from hashlib import md5

obj = md5()
obj.update("xxxx".encode("utf-8"))
v1 = obj.digest()  # 得到是加密之后的字节
print(v1)  # b'\xeaAn\xd0u\x9dF\xa8\xdeX\xf6:Y\x07t\x99'
v2 = obj.hexdigest()  # 将加密之后的字节转成十六进制字符串
print(v2)  # ea416ed0759d46a8de58f63a59077499



