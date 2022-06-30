import re
import os
import time
import requests
import asyncio
import aiohttp
import aiofiles
from lxml import etree
from urllib.parse import urljoin
from Crypto.Cipher import  AES  # pip install pycryptodome

"""
整体步骤
1.想办法找到M3U8文件
2.判别是否需要下载第二层M3U8
3.提取ts文件的下载路径
4.下载
5.判别是否需要解密
6.如果需要解密，拿到密钥
7.解密
8.根据M3U8正确顺序来合并所有的ts文件==>MP4
"""
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
}


def get_iframe_src(url):
    resp = requests.get(url, headers=headers)
    root = etree.HTML(resp.text)  # type: etree._Element
    src = root.xpath("//iframe/@src")[0]
    return src


def get_m3u8_url(url):
    resp = requests.get(url, headers=headers)
    obj = re.compile(r'url: "(?P<m3u8>.*?)"')
    m3u8 = obj.search(resp.text).group("m3u8")
    return m3u8


def download_m3u8(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers)
    with open("first.m3u8", mode="w", encoding="utf-8") as f:
        f.write(resp.text)
    with open("first.m3u8", mode="r", encoding="utf-8") as f2:
        for line in f2:
            if line.startswith("#"):
                continue
            # 此时的line就是第二层M3U8的地址
            line = line.strip()  # 有换行存在，要去掉
            line = urljoin(url, line)
            resp = requests.get(line, headers=headers)
            with open("second.m3u8", mode="w", encoding="utf-8") as f3:
                f3.write(resp.text)
                # break


async def download_one(url, sem):
    # 使用信号量控制访问频率
    async with sem:
        file_name = url.split("/")[-1]
        file_path = f"./解密前/{file_name}"
        print(f"{file_name}，开始下载")
        for i in range(10):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers) as resp:
                        content = await resp.content.read()
                        # 写入文件
                        async with aiofiles.open(file_path, mode="wb") as f:
                            await f.write(content)
                print(f"{file_name}，下载完成")
                break
            except Exception as e:
                print(f"{file_name}, 处理失败：{e}")
        else:  # 如果10次都没有请求成功，记录一下Url，可以重新再跑一次
            with open("./encrypt_m3u8.log") as f:
                f.write(url)
                f.write("\n")


async def download_all_videos():
    # 信号量，用来控制协程的并发量
    sem = asyncio.Semaphore(100)  # 网吧电影中极个别电影需要控制在5左右
    # 1.读取文件
    tasks = []
    with open("second.m3u8", mode="r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            # 此时，line就是下载地址
            line = line.strip()  # 这里一定要加上，每次都要强调
            # 2.创建任务
            t = asyncio.create_task(download_one(line, sem))
            tasks.append(t)
    # 3.统一等待
    await asyncio.wait(tasks)


def get_key():
    with open("second.m3u8", mode="r", encoding="utf-8") as f:
        file_content = f.read()  # 读取到所有内容
        obj = re.compile(r'URI="(?P<key_url>.*?)"')
        key_url = obj.search(file_content).group("key_url")
        # print(key_url)
        resp = requests.get(key_url, headers=headers)
        # 直接拿字节，为了解密的时候，直接丢进去就可以了
        return resp.content


async def decrypt_one(key, file_name):
    async with aiofiles.open(f"./解密前/{file_name}", mode="rb") as f1, \
            aiofiles.open(f"./解密后/{file_name}", mode="wb") as f2:
        content = await f1.read()
        # 解密
        # 固定逻辑，创建一个加密器
        aes = AES.new(key=key, mode=AES.MODE_CBC, IV=b"0000000000000000")
        new_content = aes.decrypt(content)
        await f2.write(new_content)


# 解密的协程逻辑
# 读second.m3u8文件，拿到文件名称和路径
# 每个ts文件一个任务
# 在每个任务中解密即可
async def decrypt_all_videos(key):
    tasks = []
    with open("second.m3u8", mode="r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            line = line.strip()
            file_name = line.split("/")[-1]
            # 创建任务，去解密
            t = asyncio.create_task(decrypt_one(key, file_name))
            tasks.append(t)
    await asyncio.wait(tasks)


def merge():
    # 视频片段合成（B站视频，不适用这个，要用ffmpeg）
    # 需要一个命令
    # windows：copy /b a.ts+b.ts+c.ts "xxx.mp4"
    # linux/mac：cat a.ts b.ts c.ts > xxx.mp4
    # 共同的坑：
    # 1.执行命令 太长了，需要分段合并
    # 2.指定命令的时候，容易出现乱码，采用popen来执行命令，就可以避免乱码
    # 3.你只需关注，是否合并成功？
    # os.system("dir")
    # r = os.popen("dir", )
    # print(r.read().encode("gbk", "ignore").decode("gbk", "ignore"))
    # print(r.read())

    # 分段合并
    # 合并, 要考虑顺序
    file_list = []
    with open("second.m3u8", mode="r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            line = line.strip()
            file_name = line.split("/")[-1]
            file_list.append(file_name)
    # 进入到文件夹内
    os.chdir("./解密后")  # 更换工作目录
    # file_list 所有文件名称
    n = 1
    temp = []
    for i in range(len(file_list)):
        # 每20个合并一次
        file_name = file_list[i]
        temp.append(file_name)
        if i != 0 and i % 20 ==0:
            # 可以合并一次了
            cmd = f"copy /b {'+'.join(temp)} {n}.ts"
            r = os.popen(cmd)
            print(r.read())
            for j in range(len(temp)):
                file_name = temp.pop()
                os.popen(f"del /F /S /Q {file_name}")
            # temp = []  # 新列表
            n += 1
    if temp:
        cmd = f"copy /b {'+'.join(temp)} {n}.ts"
        r = os.popen(cmd)
        print(r.read())
        for j in range(len(temp)):
            file_name = temp.pop()
            os.popen(f"del /F /S /Q {file_name}")

    # 第二次合并
    last_temp = []
    for i in range(1, n + 1):
        last_temp.append(f"{i}.ts")
    cmd = f"copy /b {'+'.join(last_temp)} 春夏秋冬又一春.mp4"
    r = os.popen(cmd)
    print(r.read())
    for j in range(len(last_temp)):
        file_name = last_temp.pop()
        os.popen(f"del /F /S /Q {file_name}")
    # 回来
    os.chdir("../")  # ../ 上层文件夹


async def merge_file():
    os.chdir("./解密后")
    async with aiofiles.open("../second.m3u8", mode="r", encoding="utf-8") as f1, \
        aiofiles.open("春夏秋冬又一春.mp4", mode="ab") as f2:
        lines = await f1.readlines()
        for line in lines:
            if line.startswith("#"):
                continue
            line = line.strip()
            file_name = line.split("/")[-1]
            async with aiofiles.open(file_name, mode="rb") as f3:
                await f2.write(await f3.read())
            os.popen(f"del /F /S /Q {file_name}")
    print("合并完成")
    os.chdir("../")


def main():
    url = "http://www.wbdy.tv/play/63690_1_1.html"
    # 1.拿到iframe的src属性值
    src = get_iframe_src(url)
    print(src)
    # 2.发送请求到iframe的src路径，获取M3U8地址
    src = urljoin(url, src)
    m3u8_url = get_m3u8_url(src)
    print(m3u8_url)
    # 3.下载m3u8文件
    download_m3u8(m3u8_url)
    # 4.下载视频.上协程下载视频
    download_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(download_loop)
    download_loop.run_until_complete(download_all_videos())
    download_loop.close()
    # 5.拿密钥
    key = get_key()
    print(key)
    # 6.解密
    decrypt_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(decrypt_loop)
    decrypt_loop.run_until_complete(decrypt_all_videos(key))
    decrypt_loop.close()
    print("解密完成")
    # 7.合成
    # merge()
    # 扩展，协程写入文件
    file_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(file_loop)
    file_loop.run_until_complete(merge_file())
    file_loop.close()

if __name__ == '__main__':
    s1 = time.time()
    main()
    s2 = time.time()
    print(s2 - s1)
