from hashlib import md5

obj = md5()
obj.update("123456".encode("utf-8"))
print(obj.hexdigest())
# e10adc3949ba59abbe56e057f20f883e
# e10adc3949ba59abbe56e057f20f883e
