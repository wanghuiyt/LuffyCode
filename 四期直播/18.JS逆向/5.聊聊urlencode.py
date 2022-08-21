from urllib.parse import urlencode, quote, unquote

# 把数据转化成 urlencode => 处理的是字典
dic = {
    "name": "周杰伦=昆凌",
    "age": 18
}

# 类似于request.get(url, params=dic)
r = urlencode(dic)  # 如果需要对字典进行处理，使用urlencode处理即可
print(r)

# quote必会，把字符串直接进行urlencode处理的方法
s = "周润发喜欢我"
print(quote(s))

# 在平时逆向的时候，url一般不用手工处理，参数也不用手工处理
# 但是，在处理cookie的时候，需要手工处理
# cookie的值已经拿到了，但是里面可能会有一些必须要处理的字符（=。空格，冒号）

# 写代码还原
s = "%E5%91%A8%E6%B6%A6%E5%8F%91%E5%96%9C%E6%AC%A2%E6%88%91"
print(unquote(s))

# 直接百度： https://tool.chinaz.com/tools/urlencode.aspx
