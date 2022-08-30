import random

data = random.randbytes(10)  # python3.9
ele_list = []
for item in data:
    ele_list.append(hex(item)[2:])
res = "".join(ele_list)
print(res)

data = "".join([hex(item)[2:] for item in random.randbytes(10)])
print(data)

# 小补充，有的十六进制数不足两位，要补足

data = random.randbytes(10)
ele_list = []
for item in data:
    ele_list.append(hex(item)[2:].rjust(2, "0"))
res = "".join(ele_list)
print(res)

data = "".join([hex(item)[2:].rjust(2, "0") for item in random.randbytes(10)])
print(data)

# 十六进制 字符串格式化
v2 = "%x" % (199,)
v3 = "%02x" % (5,)
print(v2, v3)

# 关于时间戳
# 在请求头中的时候，一定是字符串类型的，不能是int类型
