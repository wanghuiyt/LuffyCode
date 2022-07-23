import pymysql

# 1.创建连接
# 默认是开启事务的
conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="root",
    database="luffy"
)

# 2.创建cursor，游标 -> 执行sql语句，以及获取sql执行结果
cur = conn.cursor()
# 3.准备好sql语句
sql = "select * from stu"
# 4.执行这个sql语句
result = cur.execute(sql)
print(result)
# 5.提交事务
# conn.commit()  # 查询不需要提交事务
# conn.rollback()  # 回滚

cur.close()  # 断开cursor
conn.close()  # 断开连接
