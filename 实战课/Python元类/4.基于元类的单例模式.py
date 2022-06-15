class MyType(type):
    def __init__(self, name, base, attrs):
        super().__init__(name, base, attrs)
        self.instance = None

    def __call__(self, *args, **kwargs):
        # 1.判断是否已有对象，有，则不创建；没有，则创建
        if not self.instance:
            self.instance = self.__new__(self)
        # 2.调用自己那个类 __init__ 方法去初始化
        self.__init__(self.instance, *args, **kwargs)
        return self.instance


class Singleton(object, metaclass=MyType):
    pass


class Foo(Singleton):
    # 类变量,创建的对象
    pass


# print(Foo.instance)

v1 = Foo()  # 真正去创建对象并设置instance & 返回
v2 = Foo()

# 内存地址一样
print(v1)
print(v2)

