# base64 => 由大写字母，小写字母，数字0-9，以及/和+组成 -> 64个符号
# base64 把字节变成字符串  把字符串还原成字节
# base64处理的时候，三个字节一起处理 -> 处理成4个字符
# base64处理后的字节 会比原来大一点点

import base64

s = "我爱你"
# 转化成字节
bs = s.encode("utf-8")
print(bs)
# 转成成base64字符串
b64_str = base64.b64encode(bs)
b64_str = b64_str.decode()  # 这里是Unicode编码，不需要encoding
print(b64_str)

# 如果有了b64字符串，还原字节
s = "5oiR54ix5L2g"
bs = base64.b64decode(s)
print(bs)

# base64的字符串本质是什么？ 字节
# 所有的告诫加密逻辑里，大部分都是字节
