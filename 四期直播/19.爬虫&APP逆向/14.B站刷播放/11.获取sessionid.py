import random

# python3.9 以上才能运行
# session_id = "".join([hex(item)[2:] for item in random.randbytes(4)])
session_id = "".join([hex(random.randint(0, 255))[2:] for i in range(4)])
print(session_id)

# b函数
arg8 = "205bad13903f157d158794906af38eb620220910125022820181316256436c"
g= 0
h= 60
i2= 2
v5 = 0
while True:
    v6 = arg8[g: g+2]
    v5 += int(v6, base=16)
    if g != h:
        g += i2
        continue
    break
data = "%02x" % (v5 % 0x100,)
print(data)