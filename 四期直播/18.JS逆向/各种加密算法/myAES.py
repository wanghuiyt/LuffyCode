"""
pip install pycrypto
pip install pycryptodome
"""
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# s = "我喜欢你好久了，保密啊"
# key = b'1234567890abcdef'
"""
模式：
    AES.MODE_ECB，该模式下不需要给iv(偏移量)
    AES.MODE_CBC，该模式下需要给iv 数据加密之前会被添加偏移量
key:
    最少16(AES-128)位的长度，24(AES-192) 32(AES-256)
iv:
    偏移量，一般与key的长度一致
"""
# iv = key[::-1]
# # aes = AES.new(key=key, mode=AES.MODE_ECB)
# aes = AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
# bs = s.encode("utf-8")
# # 需要对数据进行填充,不填充会报错
# # Data must be aligned to block boundary in ECB mode
# bs = pad(bs, 16)
# result = aes.encrypt(bs)
# print(result)
# ecb_bs = b'+\x19\xf7\xe1\x02\xc8\xfbh\xa3\xeb\x96\x81"\xdb\x9e\xf3+# r\t\x14iE0\xdd%\x1c\xdfVW=F\xc1\xd0\xd0\xedh\xe9\x1d\xcfW\xf7d,\xf7R\xd3'
# # 注意，被加密的内容，不能用gbk，utf-8进行处理，它是乱的
# cbc_bs = b'\xfav~q\xf1A\xab;T~y\x8fcy\x83\xa9q\xfc%\x84:\xea\t\x1f\xe4\xa3ui\xdf\xc44\xd3x\xb8\xed\x9e4\xa3^**\xfde\xa0L\xa5\\\xeb'
#
# b64_str = base64.b64encode(result).decode()
# print(b64_str)

# 前端接收到的
ss = "+nZ+cfFBqztUfnmPY3mDqXH8JYQ66gkf5KN1ad/ENNN4uO2eNKNeKir9ZaBMpVzr"
# 解密逻辑
key = b'1234567890abcdef'
iv = key[::-1]
aes = AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
# 对b64处理成字节，然后才开始解密
b64_bs = base64.b64decode(ss)
print(b64_bs)  # b'\xfav~q\xf1A\xab;T~y\x8fcy\x83\xa9q\xfc%\x84:\xea\t\x1f\xe4\xa3ui\xdf\xc44\xd3x\xb8\xed\x9e4\xa3^**\xfde\xa0L\xa5\\\xeb'
# res = aes.decrypt(b64_bs).decode()  # 我喜欢你好久了，保密啊
res = aes.decrypt(b64_bs)  # b'\xe6\x88\x91\xe5\x96\x9c\xe6\xac\xa2\xe4\xbd\xa0\xe5\xa5\xbd\xe4\xb9\x85\xe4\xba\x86\xef\xbc\x8c\xe4\xbf\x9d\xe5\xaf\x86\xe5\x95\x8a\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f'
# 对加密数据去除填充
res = unpad(res, 16).decode("utf-8")  # 我喜欢你好久了，保密啊
print(res)


