import asyncio
import aiohttp
import aiofiles


async def download(url):
    print("我要开始下载了", url)
    file_name = url.split("/")[-1]
    # 我要发送请求
    # 如果with后面用的是一个异步的包，那么绝大多数这前面要加async
    async with aiohttp.ClientSession() as session:  # 理解： session = requests.session()
        async with session.get(url, headers={}) as resp:  # resp = session.get()
            # 等待服务器返回结果了

            # 获取页面源代码
            # page_source = await resp.text(encoding="utf-8")

            # 需要json
            # dic = await resp.json()

            # 字节
            content = await resp.content.read()

            # 有了结果要干嘛？
            # 在异步协程中，可以使用同步代码
            # 可以用open，但是比较慢
            # with open(file_name, mode="wb") as f:
            #     f.write(content)
            async with aiofiles.open(file_name, mode="wb") as f:
                await f.write(content)
    print(f"{file_name} 下载完成")


async def main():
    urls = [
        "https://www.xiurenji.vip/uploadfile/202110/20/1F214426892.jpg",
        "https://www.xiurenji.vip/uploadfile/202110/20/91214426753.jpg"
    ]
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(download(url)))
    await asyncio.wait(tasks)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
