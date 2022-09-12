import time
import random
from hashlib import sha1


def sha1_encrypt(data_string):
    obj = sha1()
    obj.update(data_string.encode("utf-8"))
    return obj.hexdigest()


if __name__ == '__main__':
    ctime = int(time.time() * 1000)
    cnum = random.randint(100000, 1000000)
    res = sha1_encrypt(f"{ctime}{cnum}")
    print(res)





