"""
负责代理IP的校验工作
"""
import asyncio
import time

import aiohttp
from proxy_redis import ProxyRedis
from multiprocessing import Process

r = ProxyRedis()


async def verify_one(ip, sem):
    print(f"开始检测{ip}的可用性...")
    # 设置超时时间为10s
    timeout = aiohttp.ClientTimeout(total=10)
    async with sem:
        try:
            async with aiohttp.ClientSession() as session:
                # requests.get(url, proxies={"http": "http://192.168.1.1:3000"})
                async with session.get("http://www.baidu.com/s?wd=ip", proxy=f"http://{ip}", timeout=timeout) as resp:
                    _ = await resp.text()
                    if resp.status in [200, 302]:
                        r.set_max_score(ip)
                        print(f"检测到{ip}，是可用的，分值拉满")
                    else:
                        r.desc_incrby(ip)
                        print(f"{ip}, 本次不可以，要扣分了")
        except Exception as ex:
            r.desc_incrby(ip)
            print(f"检测{ip}，出现异常,", ex)

# 用协程最合适
async def main():
    # 1.把ip全部查出来
    all_proxies = r.get_all_proxy_ip()
    # 2.挨个发送请求，如果能正常返回，分值拉满，否则，扣分
    sem = asyncio.Semaphore(30)  # 添加一个信号量
    tasks = []
    for ip in all_proxies:
        tasks.append(asyncio.create_task(verify_one(ip, sem)))
    if tasks:
        await asyncio.wait(tasks)


def run():
    time.sleep(10)
    while True:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main())
            time.sleep(100)
        except Exception as e:
            print("在校验的时候报错了,", e)


if __name__ == '__main__':
    p = Process(target=run)
    p.start()


