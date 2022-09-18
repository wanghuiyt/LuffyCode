import random

# open_udid = "".join([hex(i)[2:] for i in random.randbytes(10)])
open_udid = "".join([hex(random.randint(0, 255))[2:] for _ in range(10)])
print(open_udid)
