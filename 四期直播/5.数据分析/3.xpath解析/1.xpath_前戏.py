from lxml import etree

# 准备一段html
f = open("index.html", mode="r", encoding="utf-8")
content = f.read()  # 页面源代码

# 以后写代码，没提示怎么办？
# 用type()查看数据类型
# 去变量被赋值位置，添加 # type: 类型

# 1.etree.HTML(页面源代码) 相当于 BeautifulSoup(页面源代码)
# 默认Pycharm不知道什么类型，没有代码提示
page = etree.HTML(content)  # type: etree._Element # 给Pycharm看的
# print(main_page)  # <Element html at 0x11aebab8100>
# print(type(page))  # <class 'lxml.etree._Element'>
# xpath()筛选

# 语法1：根节点
# / 出现在开头，表示根节点
# xpath得到的结果永远永远是列表
# root = page.xpath("/html")
# print(root)  # [Element xxx at xxx]
# print(type(root))  # list

# / 出现在中间是直接子节点，不是孙子节点
# p = page.xpath("/html/body/div/p")
# print(p)   # [Element p at xxx]

# / 出现在中间，也有可能是找某个节点内部的东西
# text()表示提取内部的文本
# p = page.xpath("/html/body/div/p/text()")
# print(p)  # ['一个很厉害的人']

# // 提取的后代节点
# s = page.xpath("/html/body/div/p//text()")
# print(s)

# // 出现在开头表示提取整个页面 查找子节点 /p表示所有子节点中的p
# divs = page.xpath("//div/p/text()")
# print(divs)

# 在xpath中 [] 里面可以给出位置，位置是从1开始数的
# zi = page.xpath("//ol/ol/li[2]/text()")
# print(zi)

# 提取第三个li的文本，不是第三个位置是li的文本
# r = page.xpath("//li[3]/text()")
# print(r)
