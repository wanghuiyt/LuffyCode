# 字节列表
byte_list = [-26, -83, -90, -26, -78, -101, -23, -67, -112]

"""
java字节：有符号 -128~127
python: 无符号 0~255 
"""

# 字节列表->python的字节数组
bs = bytearray()
for item in byte_list:
    if item < 0:
        item += 256  # Java中是有符号的，python中是无符号的
    bs.append(item)

# python的字节数组 -> 编码 -> 字符串
str_data = bs.decode("utf-8")  # data = bytes(bs)
print(str_data)

# 字符串转字节数组
data = "张三懵逼了"
data_bytes = data.encode("utf-8")

data_list = bytearray()
for item in data_bytes:
    data_list.append(item)

print(data_list)
res = data_list.decode("utf-8")
print(res)

# 另一种写法
byte_list = [-26, -83, -90, -26, -78, -101, -23, -67, -112]
data_list = []
for item in byte_list:
    item = item & 0xff  # item<0时，让item+256
    ele = "%02x" % item
    data_list.append(ele)
print("".join(data_list))

