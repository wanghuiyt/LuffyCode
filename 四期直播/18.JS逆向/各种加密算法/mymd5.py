from hashlib import md5

"""
查询MD5：https://cmd5.com/
obj是一次性的
默认的MD5是有问题的，有可能会出现 撞库 的现象(有人将大量计算的md5值存入数据，可以查询到就返回明文)
    可以在使用md5的时候，撒盐用来对抗撞库问题
sha1 sha256 sha512 和 md5 是一样的用法
"""

# # 创建一个MD5对象，可以在使用md5的时候，撒盐用来对抗撞库问题
# # obj = md5(b'nihaoasfjdsfhldfgkcjvbcmbsadfw')
# obj = md5()
# # 准备要计算的东西->字节
# # name = "alex".encode("utf-8")
# name = "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36".encode("utf-8")
# # 把数据丢给obj
# obj.update(name)
# # 导出md5值
# val = obj.hexdigest()
# print(val)
# 5e51a7f12b0d6d56acf3f233a5c53a78
# 534b44a19bf18d20b71ecc4eb77c572f 固定长度32位

def md5_sign(data: str, secret=""):
    obj = md5(secret.encode("utf-8"))
    obj.update(data.encode("utf-8"))
    return obj.hexdigest()


if __name__ == '__main__':
    sign = md5_sign("5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36")
    print(sign)
