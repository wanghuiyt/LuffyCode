from lxml import etree

f = open("index.html", mode="r", encoding="utf-8")
content = f.read()

page = etree.HTML(content)  # type: etree._Element

# 属性上的限定
# xpath语法中 @属性 = 值
# r = page.xpath("//ol/li[@id='10086']/text()")
# r = page.xpath("//li[@id='10086']/text()")
# print(r)

# 这里写class属性选择的时候，直接复制即可(页面源代码)
# j = page.xpath("//li[@class='jay haha']/text()")
# print(j)

# 这里的*表示的是单个任意标签
# j = page.xpath("//*[@class='jay haha']/text()")
# print(j)

# x = page.xpath("//div/*/span/text()")
# print(x)

# 只要标签中有class属性的都会被提取
# x = page.xpath("//*[@class]/text()")
# print(x)

# 拿到ul中每一个href
# 方案一：后续的操作和该页面没有其他关系了
# @href 表示的是拿href的值
# href = page.xpath("//ul/li/a/@href")
# # print(href)
# for h in href:
#     print(h)

# 方案二：可扩展性比较好
# a_list = page.xpath("//ul/li/a")
# print(a_list)
# for a in a_list:
#     href = a.xpath("./@href")[0]  # ./ 表示当前节点，不写会雪崩
#     text = a.xpath("./text()")
#     if text:
#         text = text[0]
#     else:
#         text = "123"
#     print(text, href)

li = page.xpath("//body/ol/li[last()]/a/text()")  # last() 拿到最后一个
print(li)



