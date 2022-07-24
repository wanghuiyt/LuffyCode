"""
负责该项目中所有的关于redis的操作
"""
import random
from redis import Redis


class ProxyRedis:
    """
    需要的功能：
        1.存储
            不能直接进行存储，先判断是否存在该IP，如果存在，就不进行新增操作
        2.需要校验所有的IP
            查询所有IP
        3.ip可用，分值拉满
        4.ip不可用，扣分
        5.查询可用的代理IP
            先给满分的
            没有满分的给有分的（>10）
            还有就不给
    """
    def __init__(self):
        self.name = "proxy_ip"
        self.redis = Redis(
            host="localhost",
            port=6379,
            password="123456",
            db=0,
            decode_responses=True
        )

    def add_proxy_ip(self, ip):
        # 1.先判断是否存在IP
        if not self.redis.zscore(self.name, ip):
            self.redis.zadd(self.name, {ip: 10})

    def get_all_proxy_ip(self):
        return self.redis.zrange(self.name, 0, -1)

    def set_max_score(self, ip):
        self.redis.zadd(self.name, {ip: 100})

    def desc_incrby(self, ip):
        # 先查询分值
        score = self.redis.zscore(self.name, ip)
        # 如果分值还有，扣1分
        if score and score > 0:
            self.redis.zincrby(self.name, -1, ip)
        else:
            # 如果分值已经扣没了，可以再见了
            self.redis.zrem(self.name, ip)

    def get_enable_proxy(self):
        ips = self.redis.zrangebyscore(self.name, 100, 100, 0, -1)
        if ips:
            return random.choice(ips)
        else:
            ips = self.redis.zrangebyscore(self.name, 11, 99, 0, -1)
            if ips:
                return random.choice(ips)
            else:
                print("实在是没有能拿得出手的ip了")
                return None

    def save(self):
        self.redis.save()

    def close(self):
        self.redis.close()


if __name__ == '__main__':
    proxy = ProxyRedis()
    proxy.get_all_proxy_ip()
