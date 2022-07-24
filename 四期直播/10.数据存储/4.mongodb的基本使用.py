import pymongo

# 1.创建连接
conn = pymongo.MongoClient(host="localhost", port=27017)
# 2.选择数据库
db = conn["python_2"]  # use python_2
# 3.开始操作
# db.stu.insert_one({"name": "alex"})
# db.stu.insert_many([{"name": "sylar"}, {"name": "tory"}, {"name": "relay"}])

# 查询
# 第一个{}是查询条件
# 第二个{}是投影，查询哪些字段就写1，_id可以写0，与其他字段一起使用，其余字段要么全是1，要么全是0
result = db.stu.find({}, {"_id": 0, "name":1})
# print(dir(result))
for item in result:
    print(item)


