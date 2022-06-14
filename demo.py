import re
import random
import string
from faker import Faker

"""
即使深陷泥潭，也要仰望星空
王侯将相宁有种乎，坚信自己一定能成事
你只需多走一步，你就超越了多数人
没有对比就不知道自己身处井底
很多人身处温水而不自知
"""

"""
猜年龄小游戏
"""
# correct_age = 25
#
# while True:
#     input_age = input("请输入一个年龄：")
#     if input_age.isdigit():
#         input_age = int(input_age)
#     else:
#         print("无法识别输入年龄，游戏结束!")
#
#     if input_age > correct_age:
#         print("猜的太大了，往小里试试...")
#     elif input_age < correct_age:
#         print("猜的太小了，往大里试试...")
#     else:
#         print("恭喜你，猜对了...")
#         break
# print("游戏结束!")

"""
猜年龄进阶版
三次之后如果还想玩，输入y
"""
# count = 0
# correct_age = 25
# while count < 3:
#     input_age = input("请输入年龄：")
#     if input_age.isdigit():
#         input_age = int(input_age)
#     else:
#         print("请输入正确的年龄")
#         continue
#
#     if input_age > correct_age:
#         print("往小了猜")
#     elif input_age < correct_age:
#         print("往大了猜")
#     else:
#         print("猜对了")
#         break
#     count += 1
#     if count == 3:
#         cmd = input("输错三次，还要不要玩(y/n)?").strip()
#         if cmd.lower() == "y":
#             count = 0
#         else:
#             print("bye bye...")

"""
写一段程序，读取用户输入的工资
根据工资多少打印下面对应的文字
"""
# msg_dict = {
#     "1000": "老板，我是你爹",
#     "2000": "老板，wqieqpwieyqp",
#     "5000": "老板脑子有坑，背后说坏话",
#     "10000": "老板说的有点问题，但是我不说话",
#     "20000": "老板说啥就是啥吧，给钱就行",
#     "30000": "老板说什么都是对的，如果有人错了，那一定是我",
#     "50000": "996就像呼吸一样自然",
#     "100000": "公司就是我家"
# }
#
# salary = input("请输入你的月薪：")
# print(msg_dict.get(salary, "你没有资格说话"))

"""
打印奇偶数
"""
# for i in range(100):
#     if i % 2 == 0:
#         print(i)

"""
循环嵌套
"""
# for floor in range(1, 7):
#     print(f"当前在{floor}层".center(50, '-'))
#     for room in range(1, 10):
#         print(f"当前房间是{floor}0{room}室")

"""
楼层打印进阶
continue & break 只能结束当前层的循环
"""
# for i in "alex jack":
#     print(i)
# print(i)  # 此时的i仍然是k

# for floor in range(1, 7):
#     print(f"当前在{floor}层".center(50, '-'))
#     if floor == 3:
#         print("不走三层...")
#         continue
#     for room in range(1, 10):
#         if floor == 4 and room == 4:
#             print("见鬼了...")
#             break
#             # exit()
#         print(f"当前房间是{floor}0{room}室")

"""
99乘法表
"""
# for i in range(1,10):
#     for j in range(1,i+1):
#         print(f"{i}x{j}={i*j}", end=" ")
#     print()

"""
素数练习
一个大于1的正整数，如果除了1和它本身以外，不能被其他正整数整除，就叫素数
"""
# for i in range(1, 101):
#     is_prime = True
#     for j in range(2, i):
#         if i % j == 0:
#             is_prime = False
#     if is_prime:
#         print(i, end=" ")

"""
素数练习进阶版
"""
# for i in range(1, 101):
#     for j in range(2, i):
#         if i % j == 0:
#             break
#     else:
#         print(i, end=" ")

"""
打印三角形
"""
# for i in range(11):
#     if i == 0 or i == 10:
#         continue
#     if i <= 5:
#         print("* " * i)
#     else:
#         print("* " * (10 - i))

"""
for/while ... else
当程序正常结束时，会执行else的代码
代码被break exit结束时，不再执行else代码
"""
# for i in range(10):
#     print(i)
#     if i == 5:
#         break
# else:
#     print("loop done...")
# print("done")

"""
存款多少年才能翻倍？
1万本金，利息0.0325每年，问连本带息多少年能翻倍？
"""
# base = 10000
# interest = 0.0325
# year = 0
# while base <= 20000:
#     year += 1
#     base += base * interest
# else:
#     print(year, base)

"""
小球坠落长度计算
"""
# height = 100
# distance = 0
# count = 0
# while count < 10:
#     distance += height
#     height /= 2
#     distance += height
#     count += 1
#     print(count, distance, height)
#
# for i in range(1, 11):
#     height /= 2
#     distance += height * 3
#     print(i, distance, height)

"""
猴子吃桃
有一堆桃子，猴子每天吃桃子总数的一半并多吃一个，吃了10天，到第11天只剩一个桃子，问，猴子吃之前，一共是多少个桃子
"""
# num = 1
# for i in range(1, 11):
#     num = (num + 1) * 2
# print(f"桃子总数是:{num}")

"""
计算从1-2+3-4+5-6+7....100的和
"""
# sum_num = 0
# for i in range(1, 101):
#     if i % 2 == 0:
#         i *= -1
#     sum_num += i
# print(sum_num)

"""
寻找列表中的最大值，最小值
"""
# data = [9, 10, 33, 4, 5, 28, 4, 24, 576, 11]
# max_n = data[0]
# min_n = data[0]
# for i in data:
#     if i > max_n:
#         max_n = i
#     if i < min_n:
#         min_n = i
# print(min_n, max_n)

"""
寻找组合
从两个列表里各取1个数，如果两个数的和等于10，则以元组的方式输出这两个数
"""
# data = [9, 10, 26, 17, 33, 3, 5, 18, 34, 4, 32, 25, 2, 11]
# data2 = [8, 3, 2, 1, -5, 19, 2, 4, 6, 7, 11]
# for i in data:
#     for j in data2:
#         if i + j == 10:
#             print((i, j))

"""
年会抽奖程序
有300名员工，开年会抽奖，奖项如下：
一等奖3名，二等奖6名，三等奖30名
规则：
共抽奖三次，第一次抽3等奖，第二次抽2等奖，第三次抽1等奖
每个员工中将一次，不能重复
"""
# names = []
# fake = Faker("zh_CN")
# for i in range(300):
#     names.append(fake.name())
#
# count = [30, 6, 3]
# for i in count:
#     name = random.sample(names, i)
#     names = list(set(names).difference(set(name)))
#     print(f"获得{3 - count.index(i)}等奖的是：{name}")

"""
文本加密小程序
"""
# source = string.printable
# output = string.printable[::-1]
# password_table = str.maketrans(source, output)
# password_table2 = str.maketrans(output, source)
# msg = "hello world"
# # 加密字符串
# encrypt_msg = msg.translate(password_table)
# # 解密字符串
# decrypt_msg = encrypt_msg.translate(password_table2)
# print(msg, encrypt_msg, decrypt_msg)

"""
统计字符、数字、特殊字符的个数
"""
# while True:
#     msg = input(">：").strip()
#     if not msg: continue
#     str_count = 0
#     int_count = 0
#     space_count = 0
#     special_count = 0
#     for i in msg:
#         if i.isalpha():
#             str_count += 1
#         elif i.isdigit():
#             int_count += 1
#         elif i.isspace():
#             space_count += 1
#         else:
#             special_count += 1
#     print(f"str count:{str_count}, int count:{int_count}, space count:{space_count}, special count:{special_count}")

"""
列表去重(不适用set)
"""
# a = [i % 2 for i in range(10)]
# b = []
# for i in a:
#     if i not in b:
#         b.append(i)
# print(b)

# li = [8, 3, 12, 1, 2, 34, 54, 12, 3, 12, 5]
# duplicate_nums = []
# for i in li:
#     i_show_count = li.count(i)
#     if i_show_count > 1 and [i, i_show_count] not in duplicate_nums:
#         duplicate_nums.append([i, i_show_count])
# for item in duplicate_nums:
#     duplicate_n, duplicate_times = item
#     for j in range(duplicate_times - 1):
#         li.remove(duplicate_n)
# print(li)

"""
找到列表中第2大的值
"""
# a = [i for i in range(10)]
# max_value = a[0]
# second_value = a[0]
# for i in a:
#     if i > max_value:
#         max_value, second_value = i, max_value
# print(f"第2大的值是：{second_value}")

# 冒泡排序，第二层循环取最大值
# a = [8, 3, 12, 1, 2, 34, 54, 12, 34, 11, 17, 18, 99, 1, 3, 5, 10]
# for n in range(len(a)):
#     for index, i in enumerate(a):
#         if index < len(a)-1 and i > a[index + 1]:
#             a[index], a[index + 1] = a[index + 1], i
# print(a)

"""
统计列表中每个值出现的次数(不能使用字典)
"""

"""
判断一个列表是不是另一个列表的子列表
"""
# a = [1, 2, 3, 4, 5, 6]
# b = [1, 2, 3, 8]
# for i in b:
#     if i not in a:
#         print("b不是a的一个子列表")
#         break
# else:
#     print("b是a的一个子列表")

"""
求出列表中，离最大值和最小值的平均值最接近的值
"""
# a = [i for i in range(11)]
# max_num = a[0]
# min_num = a[0]
# for i in a:
#     if i > max_num:
#         max_num = i
#     if i < min_num:
#         min_num = i
# else:
#     avg_num = (min_num + max_num) / 2
#     avg = a[0]
#     for i in a:
#         if abs(avg_num - i) < abs(avg_num - avg):
#             avg = i
#     print(f"离最大值和最小值平均值最接近的值是：{avg}")

"""
双色球选购程序
每一注六个红球，一个蓝球
红球：1-32
蓝球：1-16
"""
# red_balls = []
# blue_balls = []
# rules = [[6, 33, "红球", red_balls], [1, 16, "蓝球", blue_balls]]
#
# for item in rules:
#     print(f"开始选择{item[2]}".center(10, '-'))
#     count = 0
#     while count < item[0]:
#         choice = input(f"输入第{count + 1}个{item[2]}号码>:").strip()
#         if not choice.isdigit():
#             print("不合法")
#             continue
#         choice = int(choice)
#         if 0 < choice <= item[1] and choice not in item[3]:
#             item[3].append(choice)
#             count += 1
# print(red_balls, blue_balls)

"""
购物车程序（不能使用dict,set）
1.程序实现打印商品列表，用户可以通过商品编号来选购商品，允许不断的买商品
2.程序启动时，让用户先输入自己的工资，总购物的商品价格不得超过工资
3.用户随时可退出程序，退出时，打印分别买了哪些商品，及余额
"""
# goods_list = [["1", "辣条", 5], ["2", "衣服", 200], ["3", "雪糕", 10], ["4", "化妆品", 30]]
#
# total_amount = input("请输入你当前的余额>:").strip()
# reg = re.compile(r"^[-+]?[0-9]+\.?[0-9]+$")
# if not reg.match(total_amount):
#     print("输入金额不合法，无法购物")
#     exit()
# total_amount = float(total_amount)
# print("本商店所有商品如下".center(50, '-'))
#
# good_nums = []
# goods = []
# for item in goods_list:
#     good_nums.append(item[0])
#     goods.append([item[0], [item[1], item[2]]])
#     print(f"商品编号：{item[0]}，商品名称：{item[1]}，商品单价：{item[2]}")
#
# cost_amount = 0
# buy_good_list = []
# flag = True
# while flag:
#     if total_amount - cost_amount <= 0:
#         print("余额不足，本次购物结束")
#         flag = False
#         continue
#     good_num = input(f"输入对应的编号({','.join(good_nums)})>:")
#     if not good_num.isdigit():
#         print("输入商品编码不正确")
#         continue
#     if good_num not in good_nums:
#         print("本商店没有此商品")
#         continue
#     for i in goods:
#         if i[0] == good_num:
#             cost_amount += i[1][1]
#             if cost_amount <= total_amount:
#                 buy_good_list.append(i[1])
#             else:
#                 cost_amount -= i[1][1]
#                 print("余额不足，本次选购商品无效！")
#                 flag = False
#     print(f"您当前余额为{total_amount - cost_amount}")
#     msg = input("你想继续购物吗？(y/n)>:")
#     if msg.lower() == "n":
#         flag = False
# # print(buy_good_list)
#
# lists = []
# temp = []
# for item in buy_good_list:
#     name, price = item
#     if name not in temp:
#         temp.append(name)
#         lists.append([name, price, 1])
#     else:
#         for index, i in enumerate(lists):
#             if i[0] == name:
#                 lists[index][2] += 1
# # print(lists)
#
# print("欢迎下次光临".center(50, '-'))
# print("您本次购物清单如下".center(48, '-'))
# print("编号    商品名称   单价    数量    金额".ljust(50))
# for index, item in enumerate(lists):
#     name, price, quantity = item
#     print(f"{index + 1}     {name}    {price}    {quantity}    {price * quantity}".ljust(50))
# print("合计".center(52, '-'))
# print(f"总金额：{cost_amount}".rjust(50))

"""
生成一个包含100个key的字典，每个value的值不能一样
"""
# faker = Faker("zh_CN")
# print({faker.name(): i for i in range(100)})

"""
{"k0":0,"k1":1,"k2":2,"k3":3,"k4":4,"k5":5,"k6":6,"k7":7,"k8":8,"k9":9}
把这个dict中key大于5的值value打印出来
"""
# a = {"k0": 0, "k1": 1, "k2": 2, "k3": 3, "k4": 4, "k5": 5, "k6": 6, "k7": 7, "k8": 8, "k9": 9}
# for k in a:
#     if int(k[1:]) > 5:
#         print(a[k])

"""
把上面字典中value是偶数的统一改成-1
"""
# a = {"k0": 0, "k1": 1, "k2": 2, "k3": 3, "k4": 4, "k5": 5, "k6": 6, "k7": 7, "k8": 8, "k9": 9}
# for k in a:
#     if a[k] % 2 == 0:
#         a[k] = -1
# print(a)


"""
把下面列表中的值进行分类，变成dict
Input: test_list = [4,6,6,4,2,2,4,8,5,8]
Output: {4:[4,4,4],6:[6,6],2:[2,2],8:[8,8],5:[5]}
需求：值一样的要分类存在一个key里
"""
# test_list = [4, 6, 6, 4, 2, 2, 4, 8, 5, 8]
# test_dict = {}
# for item in test_list:
#     if item not in test_dict:
#         test_dict[item] = [item, ]
#     else:
#         test_dict[item].append(item)
# print(test_dict)

"""
把一段话里重复的单词去掉
Input: Python is great and Java is also great
Output: is also Java Python and great
"""
# s = "Python is great and Java is also great"
# s_list = s.split(" ")
# s_dict = dict.fromkeys(s_list)
# print(" ".join(s_dict.keys()))
# s_set = list(set(s_list))
# print(" ".join(s_set))

"""
写程序输出dict中values里的唯一值
dict = {"gfg":[5,6,7,8],"best":[6,12,10,8],"is":[10,11,7,5],"for":[1,2,5]}
结果:[1,2,5,6,7,8,10,11,12]
"""
# test_dict = {"gfg": [5, 6, 7, 8], "best": [6, 12, 10, 8], "is": [10, 11, 7, 5], "for": [1, 2, 5]}
# test_list = []
# for item in test_dict.values():
#     test_list.extend(item)
# print(list(set(test_list)))

""""
把下表中同字母异序词找出来
arr = ['cat', 'dog','tac','god','act']
结果:[['cat','tac','act'],['dog','god']]
"""
# arr = ['cat', 'dog', 'tac', 'god', 'act']
# test_dict = {}
# for item in arr:
#     i = list(item)
#     i.sort()
#     key = tuple(i)
#     if key not in test_dict:
#         test_dict[key] = [item, ]
#     else:
#         test_dict[key].append(item)
# print(list(test_dict.values()))

"""
三级菜单开发
1.可依次进入各子菜单
2.可任意一层往回退到上一层
3.可以任意一层退出程序
解决思路：
1.将每次输入的Key和当前dict写入新字典中，并将原dict替换成子dict
2.回退时使用popitem()，弹出最后一次的key,value;并将value赋值给Menu
注意：在dict中没有值的时候，popitem()会报错
"""
# menu = {
#     "北京": {
#         "海淀": {
#             "五道口": {
#                 "soho": {},
#                 "网易": {},
#                 "google": {}
#             },
#             "中关村": {
#                 "爱奇艺": {},
#                 "汽车之家": {},
#                 "youku": {}
#             }
#         },
#         "昌平": {
#             "沙河": {
#                 "路飞学城": {},
#                 "北航": {}
#             }
#         }
#     },
#     "上海": {
#         "嘉定": {},
#         "静安": {},
#     }
# }
#
#
# def foo(city_list):
#     for i in city_list:
#         print(i)
#
#
# foo(menu.keys())
#
# last_menu = {}
# while True:
#     input_key = input(">>")
#     if input_key == "q":
#         exit()
#
#     if input_key == "b":
#         if last_menu:
#             menu = last_menu.popitem()[1]
#     else:
#         last_menu[input_key], menu = menu, menu[input_key]
#     foo(menu.keys())

"""
用递归实现2分查找的算法
从列表a=[1,3,4,6,7,8,9,11,15,17,19,21,22,25,29,33,38,69,101]查找指定的值
"""


# def calc(lists, b, left, right):
#     if left > right:
#         return False
#     mid = (left + right) // 2
#     if b == lists[mid]:
#         return True
#     elif b > lists[mid]:
#         return calc(lists, b, mid + 1, right)
#     elif b < lists[mid]:
#         return calc(lists, b, left, mid - 1)
#
#
# a = [1, 3, 4, 6, 7, 8, 9, 11, 15, 17, 19, 21, 22, 25, 29, 33, 38, 69]
# res = calc(a, 10, 0, len(a))
# print(res)
