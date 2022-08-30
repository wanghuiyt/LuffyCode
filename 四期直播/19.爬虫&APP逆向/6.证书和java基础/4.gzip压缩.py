"""
抖音
第一打开：注册设备
    获取手机的设备信息 mac、androidId、iemi -> 发给抖音，读取设备信息，监测
        - 新设备：install_id  device_id new=1
        - 旧设备：install_id  device_id new=0
    1.读取设备信息： addhjgj
    2.对设备信息加密，得到密文 -> 字节
    3.密文字节 -> gzip压缩
    4.数据发送给抖音
        - 请求体：gzip压缩后的数据
        - 请求头：
            - xxx = md5(gzip压缩)
"""
import gzip

# 压缩
s_in = "我是小白".encode("utf-8")
s_out = gzip.compress(s_in)
print([i for i in s_out])

# 解压缩
res = gzip.decompress(s_out)
print(res)  # 得到的是字节
print(res.decode("utf-8"))

