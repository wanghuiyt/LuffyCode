"""
将redis安装到windows服务
redis-server.exe --service-install redis.windows.conf --loglevel verbose
卸载服务
redis-server --service-uninstall
开启服务
redis-server --service-start
停止服务
redis-server --service-stop
"""
import json
import redis

r = redis.Redis(
    host="localhost",
    port=6379,
    password="123456",
    db=0,
    decode_responses=True  # 不写它，中文是乱码
)

# r.set("alex", "大傻蛋")
# r.save()

# print(r.get("alex"))

# r.hset("wusir", "name", "武沛齐")
# r.hset("wusir", "age", 18)
# r.save()
#
# print(r.hmget("wusir", "name", "age"))

# print(r.hgetall("wusir"))

# r.lpush("stu", "jiuqu", "cool", "kunbu")
# print(r.lrange("stu",0, -1))

# r.sadd("teachers", "yingyu", "yanguilai", "xiaoming")
# print(r.smembers("teachers"))

# zset 有点坑
# r.zadd("yan", {"cool": 10, "kunmo": 20})
# print(r.zrange("yan", 0, -1))
# print(r.zrange("yan", 0, -1, withscores=True))

# 如果要存储列表或者字典或者列表嵌套字典，或者字典套列表

lst = ["张国强", "宋富贵", "徐长江"]
r.set("names", json.dumps(lst))
s = r.get("names")
lst = json.loads(s)
print(lst)

r.close()



