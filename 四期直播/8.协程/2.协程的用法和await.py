import asyncio
import time


async def func1():
    print("我是func1要开始了")
    # 模拟
    # time.sleep(1)  # 这里不能用time.sleep() 因为sleep不支持协程
    await asyncio.sleep(10)
    print("我是func1结束了")


async def func2():
    print("我是func2要开始了")
    await asyncio.sleep(5)
    print("我是func2结束了")


async def func3():
    print("我是func3要开始了")
    await asyncio.sleep(3)
    print("我是func3结束了")


async def main():
    # 创建三个协程对象
    f1 = func1()
    f2 = func2()
    f3 = func3()
    # 把三个协程对象都封装成任务对象
    t1 = asyncio.create_task(f1)
    t2 = asyncio.create_task(f2)
    t3 = asyncio.create_task(f3)
    # 等待三个任务结束
    tasks = [t1, t2, t3]
    # await 叫挂起来 => 拉出来，放外面去等着
    # 边上待着，等着完事了再回来
    await asyncio.wait(tasks)
    print(123456)


if __name__ == '__main__':
    # asyncio.run(main())
    s1 = time.time()
    # event_loop = asyncio.get_event_loop()  # 在3.10版中被弃用，改用下面的方式
    event_loop = asyncio.new_event_loop()
    # 下面这一步也是需要的，不然会报错：RuntimeError: Event loop is closed
    asyncio.set_event_loop(event_loop)  # 这一步不确定是否真的需要
    event_loop.run_until_complete(main())
    s2 = time.time()
    print(s2 - s1)
