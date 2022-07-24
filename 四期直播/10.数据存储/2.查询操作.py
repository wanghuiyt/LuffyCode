import pymysql
from pymysql.cursors import DictCursor

conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="root",
    database="luffy"
)

# 如果想看到其他数据结构，需要更换cursor
# 为了方便处理，可以用DictCursor把数据进行格式化成[{},{}]
cur = conn.cursor(DictCursor)
sql = "select * from stu"
r = cur.execute(sql)  # 查询的结果，不是直接给到你的
# print(r)

# 获取结果
# one = cur.fetchone()  # 拿一个
# print(one)

# another = cur.fetchone()  # 拿一个，继续拿的话，是接着拿
# print(another)

all = cur.fetchall()  # 拿取所有结果(返回的是元组)，如上面已经取过数据，就不会再取
# print(all)
for item in all:
    print(item)

cur.close()
conn.close()
