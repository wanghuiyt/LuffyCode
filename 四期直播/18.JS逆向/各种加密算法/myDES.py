import base64
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad  # 长度是8位

# s = "我喜欢你好久了，保密啊"
# key = b'12345678'
"""
模式：
    DES.MODE_ECB，该模式下不需要给iv(偏移量)
    DES.MODE_CBC，该模式下需要给iv 数据加密之前会被添加偏移量
key:
    8位
iv:
    偏移量，一般与key的长度一致
"""
# iv = key[::-1]
# aes = DES.new(key=key, mode=DES.MODE_ECB)
# # aes = DES.new(key=key, mode=DES.MODE_CBC, IV=iv)
# bs = s.encode("utf-8")
# # 需要对数据进行填充,不填充会报错
# # Data must be aligned to block boundary in ECB mode
# bs = pad(bs, 8)
# result = aes.encrypt(bs)
# print(result)
# ecb_bs = b'>m\xb1o\x01\xaa\x19\x0f\x8e\x85\xd8\x8e\xf6>\xc0\xe2%\xb5#\xc0\xe0x\xaf\x0f\xc6\x1f\x0b\xd1\xb0m,\xf5\x98n\xcd\xa2\xcazA5'
# # 注意，被加密的内容，不能用gbk，utf-8进行处理，它是乱的
# cbc_bs = b'DDR5c\xfd\xac\x9a\xa0\xa7\xf94>\xd6\xae@\xae\xc4\xcf,Z\x89y\xdc\x0e\xac\x10\xff\xb0\x17\xade\x1a\x01V\x84\xba}W_'
#
# b64_str = base64.b64encode(result).decode()
# print(b64_str)  # RERSNWP9rJqgp/k0PtauQK7EzyxaiXncDqwQ/7AXrWUaAVaEun1XXw==

ss = "RERSNWP9rJqgp/k0PtauQK7EzyxaiXncDqwQ/7AXrWUaAVaEun1XXw=="
# 解密逻辑
key = b'12345678'
iv = key[::-1]
aes = DES.new(key=key, mode=DES.MODE_CBC, IV=iv)
# 对b64处理成字节，然后才开始解密
b64_bs = base64.b64decode(ss)
print(b64_bs)  # b'DDR5c\xfd\xac\x9a\xa0\xa7\xf94>\xd6\xae@\xae\xc4\xcf,Z\x89y\xdc\x0e\xac\x10\xff\xb0\x17\xade\x1a\x01V\x84\xba}W_'
# res = aes.decrypt(b64_bs).decode()  # 我喜欢你好久了，保密啊
res = aes.decrypt(b64_bs)
# 对加密数据去除填充
res = unpad(res, 8).decode("utf-8")  # 我喜欢你好久了，保密啊
print(res)
