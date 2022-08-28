import re
import math
import json
import random
import time
import uuid
import requests

"""
推荐青果代理
注册链接：https://www.qg.net/?sale=viltf
"""


def gen_uuid():
    uuid_sec = str(uuid.uuid4())
    time_sec = str(int(time.time() * 1000 % 1e5))
    time_sec = time_sec.rjust(5, "0")
    return f"{uuid_sec}{time_sec}infoc"


def gen_b_lsid():
    data = ""
    for i in range(8):
        v1 = math.ceil(16 * random.uniform(0, 1))
        v2 = hex(v1)[2:].upper()
        data += v2
    result = data.rjust(8, "0")

    e = int(time.time() * 1000)
    t = hex(e)[2:].upper()

    return f"{result}_{t}"


# 运行时，IP限制 要用到代理IP
def get_tunnel_proxies():
    proxy_host = "tunnel2.qg.net:17955"
    proxy_username = ""
    proxy_pwd = ""

    return {
        "http": f"http://{proxy_username}:{proxy_pwd}@{proxy_host}",
        "https": f"http://{proxy_username}:{proxy_pwd}@{proxy_host}"
    }


def get_video_id_info(url, proxies):
    session = requests.session()
    session.proxies = proxies
    session.headers.update({
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    })
    bvid = url.split("/")[-1]
    resp = session.get(
        url=f"https://api.bilibili.com/x/player/pagelist?bvid={bvid}&jsonp=jsonp",
        proxies=proxies
    )

    cid = resp.json()["data"][0]["cid"]

    resp = session.get(
        url=f"https://api.bilibili.com/x/web-interface/view?cid={cid}&bvid={bvid}",
        proxies=proxies
    )

    res_json = resp.json()
    aid = res_json["data"]["aid"]
    view_count = res_json["data"]["stat"]["view"]
    duration = res_json["data"]["duration"]
    print(f"\n视频 {bvid}，平台播放量为：{view_count}")
    session.close()
    return aid, bvid, cid, duration, int(view_count)


def play(url, proxies):
    bvid = url.split("/")[-1]
    session = requests.session()
    session.proxies = proxies
    session.headers.update({
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    })
    resp = session.get(url)
    # print(resp.cookies.get_dict())
    data = re.search(r'__INITIAL_STATE__=(?P<page>.+);\(function', resp.text).group("page")
    data_dict = json.loads(data)
    aid = data_dict["aid"]
    cid = data_dict["videoData"]["cid"]

    _uuid = gen_uuid()
    session.cookies.set("_uuid", _uuid)

    b_lsid = gen_b_lsid()
    session.cookies.set("b_lsid", b_lsid)

    session.cookies.set("CURRENT_FNVAL", "4048")

    resp = session.get("https://api.bilibili.com/x/frontend/finger/spi")
    buvid4 = resp.json()["data"]["b_4"]
    session.cookies.set("buvid4", buvid4)
    session.cookies.set("CURRENT_BLACKGAP", "0")
    session.cookies.set("blackside_state", "0")

    resp = session.get(
        url="https://api.bilibili.com/x/player/v2",
        params={
            "aid": aid,
            "cid": cid
        }
    )
    sid = resp.cookies.get_dict()["sid"]

    ctime = int(time.time())

    resp = session.post(
        url = "https://api.bilibili.com/x/click-interface/click/web/h5",
        data={
            'aid': aid,
            'cid': cid,
            'part': '1',
            'lv': '0',
            'ftime': ctime - random.randint(100, 500),  # 浏览器首次打开时间
            'stime': ctime,
            'type': '3',
            'sub_type': '0',
            'refer_url': '',
            'spmid': "333.788.0.0",
            'from_spmid': '',
            'csrf': ''
        }
    )
    print(resp.text)


def run():
    proxies = get_tunnel_proxies()
    url = "https://www.bilibili.com/video/BV1N94y1R7K5"
    aid, bvid, cid, duration, view_count = get_video_id_info(url, proxies)
    while True:
        try:
            get_video_id_info(url, proxies)
            play(url, proxies)
            view_count += 1
            print("理论刷的播放量：", view_count)
        except Exception as e:
            pass

if __name__ == '__main__':
    run()

