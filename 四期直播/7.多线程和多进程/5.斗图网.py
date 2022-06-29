import time
import requests
from lxml import etree
from multiprocessing import Queue, Process
from concurrent.futures import ThreadPoolExecutor

# 图片确实在页面源代码中
# 但是，图片不在src里，在data-original里面
# 1.拿到页面源代码
# 2.提取data-original
# 3.下载图片

# 知识点：进程之间是不能直接通信的（操作系统层面的）
# 1.利用文件
# 2.网络映射
# 3.队列，只有multiProcess的队列可以实现多进程之间传输（底层逻辑：网络传输）


# 写一个函数，专门负责提取data-original
# 第一个进程，只负责提取url
def get_img_url(q):
    for i in range(1, 5):
        # 先考虑一页数据怎么抓取
        url = f"https://www.pkdoutu.com/photo/list/?page={i}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers=headers)
        root = etree.HTML(resp.text)  # type: etree._Element
        img_urls = root.xpath("//li[@class='list-group-item']//img/@data-original")
        for img_url in img_urls:
            # 把拿到的img_url 塞入队列
            q.put(img_url)  # 固定的
        # with ThreadPoolExecutor(16) as t:
        #     for img_url in img_urls:
        #         # print(img_url)
        #         # download_img(img_url)
        #         t.submit(download_img, img_url)
    q.put("end")


def get_img_url1(i, q):
    url = f"https://www.pkdoutu.com/photo/list/?page={i}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers)
    root = etree.HTML(resp.text)  # type: etree._Element
    img_urls = root.xpath("//li[@class='list-group-item']//img/@data-original")
    for img_url in img_urls:
        q.put(img_url)


# 这种方式请求太多，容易拿不到数据
def get_url_process(q):
    with ThreadPoolExecutor(16) as t:
        for i in range(1, 5):
            t.submit(get_img_url1, i, q)
            time.sleep(1)
        q.put("end")


# 第二个进程，只负责下载图片
def img_process(q):
    with ThreadPoolExecutor(16) as t:
        while True:  # 这边不确定有多少个，那就一直拿
            img_url = q.get()  # 没有问题，这里面，get是一个阻塞的逻辑
            if img_url == "end":
                break
            t.submit(download_img, img_url)


def download_img(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    resp = requests.get(url, headers=headers)
    # 文件名称
    file_name = url.split("/")[-1]
    with open(f"./img/{file_name}", mode="wb") as f:
        f.write(resp.content)
    print(f"{file_name} 下载完成")


if __name__ == '__main__':
    # s1 = time.time()
    # # get_img_url()
    # with ThreadPoolExecutor(16) as t:
    #     t.submit(get_img_url)
    # s2 = time.time()
    # print(s2 - s1)

    # 准备队列
    s1 = time.time()
    q = Queue()
    # p1 = Process(target=get_url_process, args=(q, ))
    p1 = Process(target=get_img_url, args=(q, ))  # 单独开辟一个内存, 加上q表示用同一块内存
    p2 = Process(target=img_process, args=(q, ))  # 单独开辟一个内存, 加上q表示用同一块内存
    p1.start()
    p2.start()
    # 等待主进程跑完
    p1.join()
    p2.join()
    s2 = time.time()
    print(s2 - s1)



