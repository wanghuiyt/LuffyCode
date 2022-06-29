import asyncio
import time
import requests


async def get_page_source(url):
    # 网络请求，requests不支持异步
    print("发送请求到", url)
    await asyncio.sleep(3)
    print("拿到页面源代码")
    return "我是页面源代码，你敢用吗？"


async def main():
    # 协程函数中可以用同步代码，不一定非要用异步代码
    urls = [
        "http://www.baidu.com",
        "https://www.google.com"
    ]
    # resp = requests.get("")
    # lxml => xpath => 子页面url(一堆)
    # urls = []
    tasks = []
    for url in urls:
        f = get_page_source(url)
        t = asyncio.create_task(f)
        tasks.append(t)
    # 如果需要返回值
    # 方案一
    # result, pending = await asyncio.wait(tasks)
    # for i in result:
    #     print(i.result())  # 拿结果， result() 定死的

    # 方案二
    results = await asyncio.gather(*tasks)  # 和await功能差不多
    for r in results:
        print(r)


if __name__ == '__main__':
    s1 = time.time()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    s2 = time.time()
    print(s2 - s1)
