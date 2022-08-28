import json
import time
import execjs
import binascii
import requests
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, parse_qs


body = """
function createGuid(){
    var t = (new Date).getTime().toString(36);
    var r = Math.random().toString(36).replace(/^0./, "");
    return "".concat(t, "_").concat(r);
};
function createQn(Vn){
    var Ne = -5516;
    var Yn = 0;
    for (Mr = 0; Mr < Vn.length; Mr++){
        var Xn = Vn["charCodeAt"](Mr);
        Yn = (Yn << Ne + 1360 + 9081 - 4920) - Yn + Xn,
        Yn &= Yn;
    }
    return Yn;
}
"""

JS = execjs.compile(body)

headers={
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "referer": "https://w.yangshipin.cn/"
}

def aes_encrypt(data_string, key, iv):
    key = binascii.a2b_hex(key)
    iv = binascii.a2b_hex(iv)
    aes = AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
    raw = pad(data_string.encode("utf-8"), 16)
    aes_bytes = aes.encrypt(raw)
    return binascii.b2a_hex(aes_bytes).decode()


def create_ckey(vid, ctime, app_ver, platform, guid):
    ending = "https://w.yangshipin.cn/|mozilla/5.0 (windows nt ||Mozilla|Netscape|Win32|"
    data_list = ["", vid, ctime, "mg3c3b04ba", app_ver, guid, platform, ending]
    data_string = "|".join(data_list)
    qn = JS.call("createQn", data_string)
    encrypt_string = f"|{qn}{data_string}"
    es = aes_encrypt(encrypt_string, "4E2918885FD98109869D14E0231A0BF4", "16B17E519DDD0CE5B79D7A63A4DD801C").upper()
    ckey = f"--01{es}"
    return ckey


def  get_video_info(vid, app_ver, platform, flow_id, guid, ckey):
    params = {
        "callback": "jsonp1",
        "guid": guid,
        "platform": platform,
        "vid": vid,
        "defn": "auto",
        "charge": "0",
        "defaultfmt": "auto",
        "otype": "json",
        "defnpayver": "1",
        "appVer": app_ver,
        "sphttps": "1",
        "sphls": "1",
        "spwm": "4",
        "dtype": "3",
        "defsrc": "1",
        "encryptVer": "8.1",
        "sdtfrom": platform,
        "cKey": ckey,
        "panoramic": "false",
        "flowid": flow_id
    }

    resp = requests.get(
        url="https://playvv.yangshipin.cn/playvinfo",
        params=params,
        headers=headers,
        cookies={
            "guid": guid
        }
    )
    # print(resp.text)
    text = resp.text.strip("jsonp1")[1:-1]
    # print(eval(text))
    info_dict = json.loads(text)
    # print(info_dict)
    return info_dict


def play(platform, guid, video_url, vid, pid, vurl):
    data = {
        'ctime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'ua': "mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/104.0.0.0 safari/537.36",
        'hh_ua': "mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/104.0.0.0 safari/537.36",
        'platform': platform,
        'guid': guid,
        'Pwd': "1698957057",
        'version': "wc-1.2.10",
        'url': video_url,
        'hh_ref': video_url,
        'vid': vid,
        'isfocustab': "1",
        'isvisible': "1",
        'idx': "0",
        'val': "1220",
        'pid': pid,
        'bi': "0",
        'bt': "0",
        'defn': "hd",
        'vurl': vurl,
        'step': "6",
        'val1': "1",
        'val2': "1",
        'fact1': "",
        'fact2': "",
        'fact3': "",
        'fact4': "",
        'fact5': ""
    }

    requests.post(
        url="https://btrace.yangshipin.cn/kvcollect",
        params={"BossId": 2865},
        data=data,
        headers=headers
    )


def task(video_url):
    try:
        vid = parse_qs(urlparse(video_url).query)["vid"][0]
        guid = JS.call("createGuid")
        pid = JS.call("createGuid")

        flow_id = pid
        platform = "4330701"
        app_ver = "1.2.10"
        ctime = str(int(time.time()))

        ckey = create_ckey(vid, ctime, app_ver, platform, guid)

        video_info_dict = get_video_info(vid, app_ver, platform, flow_id, guid, ckey)
        url = video_info_dict["vl"]["vi"][0]["ul"]["ui"][0]["url"]
        vkey = video_info_dict["vl"]["vi"][0]["fvkey"]
        fn = video_info_dict["vl"]['vi'][0]["fn"]

        vurl = f"{url}{fn}?sdtfrom={platform}&guid={guid}&vkey={vkey}&platform=2"

        play(platform, guid, video_url, vid, pid, vurl)
    except Exception as e:
        print(e)


def run():
    video_url = "https://w.yangshipin.cn/video?type=0&vid=i000075mu8r"
    start = time.time()
    pool = ThreadPoolExecutor(30)
    for i in range(300):
        pool.submit(task, video_url)
    pool.shutdown()
    end = time.time()

    print("执行完成，耗时：", end - start)


if __name__ == '__main__':
    run()
