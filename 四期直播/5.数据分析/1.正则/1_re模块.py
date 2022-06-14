# 在线测试：https://tool.oschina.net/regex/
import re

# r"" 专业写正则的，没有转义的烦恼
# 查找所有
# 结果 = re.findall(正则，字符串) => 返回的是列表
# result = re.findall(r"\d+", "我有1000万，不给你花，我有1块我给你")
# print(result)

# 结果 = re.finditer(正则，字符串) => 返回迭代器（需要for循环）=> 循环 => match => group()
# result = re.finditer(r"\d+", "我有1000万，不给你花，我有1块我给你")
# for it in result:
#     print(it.group())  # group分组

# 多个相同格式的结果： finditer
# 单个格式的结果：search

# 结果 = re.search(正则，字符串) 全局搜索，搜索到了，直接返回结果(返回第一个结果)
# r = re.search(r"\d+", "我有1000万，不给你花，我有1块我给你")
# print(r.group())

# complie
# obj = re.compile(r"\d+")

# result = obj.findall("我今年10岁了")
# result = obj.finditer("我今年10岁了")
# for i in result:
#     print(i.group())
# result = obj.search("我今年10岁了")
# print(result.group())

s = """
hahaha<div class='西游记'><span id='10010'>中国联通</span></div>
<div class='三国杀'><span id='10086'>中国移动</span></div>hahaha
"""

obj = re.compile("<div class='(?P<jay>.*?)'><span id='(?P<id>.*?)'>(?P<lt>.*?)</span></div>")
result = obj.finditer(s)
for i in result:
    print(i.group("jay"))
    print(i.group("id"))
    print(i.group("lt"))













