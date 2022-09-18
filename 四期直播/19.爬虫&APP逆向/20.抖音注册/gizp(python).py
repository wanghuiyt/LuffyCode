import base64
import gzip

# 压缩
s_in = "我是小明".encode("utf-8")

s_out = gzip.compress(s_in)
# print([i for i in s_out])

# 为了统一
java_gzip_body = bytearray(s_out)
java_gzip_body[3:10] = [0, 0, 0, 0, 0, 0, 0]
java_data = bytes(java_gzip_body)
print(java_data)
