"""
不论哪种sa加密，最终都是同一堆数学公式
RSA的公钥和私钥本质都是字节
"""
import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


# 使用rsa之前，必须先想办法搞到公钥或私钥
# 生成公钥私钥
# rsa_key = RSA.generate(1024)
# 此时默认拿到的是私钥
# PEM格式
"""
-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQDItP/wt/HTsQTJo+e6jmSIGcCFmOmHf1kHuwAeFQgZqOeDCqow
XJ/xPyTt9fk8shG0OSbqskmAeYQSf+y9TX2tIJdOrtWiz2EesFm6wX/pQm5/ITxF
KDGTu8hH250rBUQQsEuR+IRd7akJL4IktwDwltg1bIS5OPleBNuxbLtbEwIDAQAB
AoGAYdTgQKzY4pARvlv3k1bfJ/wtfLF5e4OWmQ8M0pz70s4i8xwasvIjQEvAK4HP
WEeQG6IUFyiKbWZN+1qBwhBopkLdDlVWIRaWBdd6KGbE+Hl2H7CjkBQG6DHqQ6wA
Z6FWrNEz6HsNFx8LC/vAPG9XEf9wr8+cjcUOjMcExPKGSrECQQDYrhqrNzoqoN2l
3YPgec8WPC3IzNe3CZEslhDbM54mvITggW1uo03SuzrwZfCmgqTdCjZ703TaP/mr
JdTn9T2rAkEA7SDdgqQzBpMBP0/gCMkC46CFnwbNTE0SaXrKeAygIN+BCsoKhKhZ
GgGJDJj7/tW/Vh+11g9MMc/78UMzWoHgOQJAYjOV9p8TB5rcmX2pdST/i+4+OdFM
urHlT7W7cf0U4i1yc2V1OT1d2fHtJmKtDGoNWfh09O3C+d8gwkZlFbN5/QJBAKLa
bGa5gDWmpjemErXV3z8XUk16LWqWj+uTIhQ6j4qkFQqk4X5j4/WhUk8tjfthLuvm
EUq27NxU+7GhNlaVVbkCQBqdaIBeg7ONgVNFxtSijxSMHo+VZjICyiCkqgRb2rip
my27E8+Bk+RM3+f1wRVLf1yoabErsIh5Z+pRWssxZ/c=
-----END RSA PRIVATE KEY-----
"""
# print(rsa_key)
# print(rsa_key.exportKey())
# print(rsa_key.exportKey(format="PEM").decode())
# print(base64.b64encode(rsa_key.exportKey(format="DER")).decode())
# 公钥可以通过私钥计算出来
# pub_key = rsa_key.public_key().exportKey("PEM")
# print(pub_key.decode())
# rsa = PKCS1_v1_5.new(rsa_key)

# 生成公钥和私钥的正确逻辑
# rsa_key = RSA.generate(2048)
# with open("rsa_private.pem", mode="wb") as f:
#     f.write(rsa_key.exportKey())
#
# pub_key = rsa_key.public_key()
# with open("rsa_public.pem", mode="wb") as f:
#     f.write(pub_key.export_key())

# 用公钥加密
# s = "你好啊，我想喝胡辣汤"
# # 获取公钥
# with open("rsa_public.pem", mode="rb") as f:
#     pub_key_bytes = f.read()
# # 将公钥进行加载，加载成rsakey类型的东西
# pub_key = RSA.importKey(pub_key_bytes)
# # print(pub_key)
# # 创建一个加密器
# rsa = PKCS1_v1_5.new(pub_key)
# bs = rsa.encrypt(s.encode("utf-8"))
# print(bs)

# 密文
ss = b'\x11\x00\x03\xb1\x0e\xceska\x8b\xe2\xdb\xf4\x87;\xde\xb3\x87\xaaF\xad|\xf1/2\x99\x0f\x94\xef0\xd6\x1e\xb1Q\x95\x8b\td\xe2yL\xd6(\x00\xefp\xe3\xa27\xbb\xef\xa6\xcc~\\\x8f[\xc3\x86S\xdd\xb2\x8f}\xd4H(+\xc0\x84\xe7Od\x7f\xe1\n\xa6\xae_\xe2\xc6\xa4\xf6\x02\x13Ze\xf3\x9f\x07\x14{\xdbd>\xfe\xc7If\x177\xc8,JlS\x02S0\xd3p\xfe"\xbf\x9f\x9d$\xa0:\xac\x8c8\x7f!OJ\xe8]\xc7G\xb4z\xdf\x08\xc6*\xe3T5V\xa5\x0f<\xaa,\xb6\x0c\xd5\xe0?\xbbjH]\xb8\x14uH%4\xb9\xb6.jL\x14\x90\xc0>\xf93\xa8P\xd5F\xd1A\xc4\\\x97\x85\x11\xf7\xc4\xea\xc6\xeb\r]\xac\x8b\xa9\xd6\xc8\xf1\xcdB\xb5k\x06\xbdy\xb1\x0fr\xb3\xd3\xc2\x19\xe6\xa3\xb5\xa7T\x95\x94\xe4,?\x83\x8a\xad+\xda\xff\x06C\xddY\xc6\xd4m%N\xd91\xbb\x89\xab\x9d\x9d\xceGL\x18Ume\x13\x0fp\x0b\xa3\xd6\xd3\xb5'
# 用私钥解密
with open("rsa_private.pem", mode="rb") as f:
    rsa_key_bytes = f.read()
rsa_key = RSA.importKey(rsa_key_bytes)
rsa = PKCS1_v1_5.new(rsa_key)
st = rsa.decrypt(ss, None)
print(st.decode("utf-8"))
