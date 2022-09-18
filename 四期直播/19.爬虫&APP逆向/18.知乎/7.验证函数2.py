import os
from hashlib import md5
from Crypto.Util.Padding import unpad

# data_string = "101_3_3.0+/api/v4/search/customize+AfBW2CEkjxWPTqU64muQ8Fhp3mqYgFVwzI4=|1663163292"
import execjs

data_string = "101_4_3.0+/udid+5.32.1+00c657fffc1a33247b7c7a15b8df54d6+AGAYsQTrkBVLBQxaWlR63dxYaCjWvOasu5M="
obj = md5()
obj.update(data_string.encode("utf-8"))
md5_str = obj.hexdigest()
print(md5_str)

with open("8.v1.js", mode="r", encoding="utf-8") as f:
    js = f.read()

# os.environ["NODE_PATH"] = r"C:\Users\ccmldl\AppData\Roaming\npm\node_modules"
ct = execjs.compile(js).call("get_sign", md5_str)
print(ct)

# 59d9f9e1e9ef9e25918f5571e0974554
# 59d9f9e1e9ef9e25918f5571e0974554

# 32022e4a64dc23d931c5ceb0747e046b
# 32022e4a64dc23d931c5ceb0747e046b
# pwSoGePL4cfGMgI189WhTR6/M2Hs4prI+KixF0VovWMCIuGSd7PZiCOHU/svhcTY