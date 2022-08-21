import random
import time

s = 2748
print(hex(s))
print(format(s, "x"))
s = "abc"
print(int(s, 16))
s = 0xabc
print(type(s))
print(s)

print(int(time.time() * 1000))
print(random.randint(0, 10))

