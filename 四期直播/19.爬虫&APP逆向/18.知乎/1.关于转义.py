import json
from urllib.parse import quote_plus, quote, unquote_plus

s = "武沛齐"

v1 = quote(s)
print(v1)
v2 = quote_plus(s)
print(v2)
v3 = unquote_plus(s)
print(v3)

# %E6%AD%A6%E6%B2%9B%E9%BD%90
# %E6%AD%A6%E6%B2%9B%E9%BD%90
# 武沛齐

# %E6%AD%A6%E6%B2%9B%E9%BD%90

info_dict = {"name": "xxx", "age": 23}
v4 = json.dumps(info_dict)
print(v4)
v5 = json.dumps(info_dict, separators=(",", ":"))
print(v5)
