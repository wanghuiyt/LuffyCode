# 发现uuid使用的是美团的热加载，继续搜索X-Sign-Token 发现uuid是读取的手机设备的device_id
# 那么就可以使用一个随机值进行验证
import random


def create_android_id(size=9):
    data_list = []
    for i in range(1, size):
        part = "".join(random.sample("0123456789ABCDEF", 2))
        data_list.append(part)
    return "".join(data_list).lower()


if __name__ == '__main__':
    res = create_android_id()
    print(res)
