import time
import random

def base36_encode(number):
    num_str = "0123456789abcdefghijklmnopqrstuvwxyz"
    if number == 0:
        return "0"
    base36 = []
    while number != 0:
        number, i = divmod(number, 36)  # 返回 number // 36  number % 36
        base36.append(num_str[i])
    return "".join(reversed(base36))

guid = base36_encode(int(time.time() * 1000)) + "_" + base36_encode(int(str(random.uniform(0, 1))[2:]))
print(guid)

