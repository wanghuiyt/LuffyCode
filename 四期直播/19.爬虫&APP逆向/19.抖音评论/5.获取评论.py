import random
import time
import uuid
from hashlib import md5

import frida
from urllib.parse import urlencode

import requests

SCRIPT = None


def get_frida_rpc_script():
    global SCRIPT
    if SCRIPT:
        return SCRIPT
    rdev = frida.get_remote_device()
    session = rdev.attach("抖音短视频")

    scr = """
    rpc.exports = {
        execandleviathan: function(i2, str){
            var result;
            Java.perform(function(){
                // 字符串->js字节->java字节

                // 先处理拼接好的数据（字节数组）
                var bArr = [];
                for(var i=0;i<str.length;i+=2){
                    var item = (parseInt(str[i],16) << 4) + parseInt(str[i+1],16);
                    bArr.push(item);
                }

                // 转换为Java字节数组
                var dataByteArray = Java.array('byte', bArr);

                // 调用leviathan方法
                var Gorgon = Java.use("com.ss.sys.ces.a");
                result = Gorgon.leviathan(-1, i2, dataByteArray);
            });
            return result;
        }
    }
    """

    script = session.create_script(scr)
    script.load()
    SCRIPT = script
    return script


def create_random_mac(sep=":"):
    """随机生成mac地址"""

    def mac_same_char(mac_str):
        v0 = mac_str[0]
        index = 1
        while index < len(mac_str):
            if v0 != mac_str[index]:
                return False
            index += 1
        return True

    data_list = []
    for i in range(1, 7):
        part = "".join(random.sample("0123456789ABCDEF", 2))
        data_list.append(part)
    mac = sep.join(data_list)
    if not mac_same_char(mac) and mac != "D4:3B:04:CE:6A:BC":
        return mac
    return create_random_mac(sep)


def create_cdid():
    return str(uuid.uuid4())


def create_openudid():
    # return "".join([hex(i)[2:] for i in random.randbytes(10)])
    return "".join([hex(i)[2:] for i in [random.randint(1, 255) for _ in range(10)]])


def md5_encrypt(data_string):
    obj = md5()
    obj.update(data_string.encode("utf-8"))
    return obj.hexdigest()


def m44417a(barr):
    data_list = []
    for item in barr:
        if item < 0:
            item += 256
        data_list.append("%02x" % item)
    return "".join(data_list)


def get_gorgon(script, param_string, cookie_string):
    # 变量a 对url参数进行MD5加密
    a = md5_encrypt(param_string)
    # 变量str7（get请求时是000.。，post请求时是x_ss_stud ）
    str7 = '00000000000000000000000000000000'
    # 变量str8，对cookie的md5加密（抓包注册设备时cookie是空的；获取评论时cookie才有值）
    if cookie_string:
        str8 = md5_encrypt(cookie_string)
    else:
        str8 = "00000000000000000000000000000000"
    # 变量str9，sessionid的md5（无）
    str9 = "00000000000000000000000000000000"

    # 拼接变量
    un_sign_string = f"{a}{str7}{str8}{str9}"

    # 执行so中的leviathan方法获取字节数组
    khronos = int(time.time())
    gorgon_byte_list = script.exports.execandleviathan(khronos, un_sign_string)

    # 调用m44417a方法获取gorgon
    gorgon = m44417a(gorgon_byte_list)
    return gorgon, khronos


def get_comment_list():
    """获取评论"""
    script = get_frida_rpc_script()
    mac_address = create_random_mac()
    cdid = create_cdid()
    openudid = create_openudid()
    _rticket = int(time.time() * 1000)
    ts = int(time.time())
    # device_id = "3831116258620196"
    # iid = "3373723980667831"

    device_id = "31209083910151"
    iid = "3655199408272903"

    # 在获取评论时，没啥用，可以删除 可以是空 可以是其他值
    ttreq = ""
    odin_tt = ""

    param_dict = {
        "aweme_id": "7144024914255793415",
        "cursor": "0",
        "count": "20",
        "address_book_access": "2",
        "gps_access": "2",
        "forward_page_type": "1",
        "channel_id": "0",
        "city": "310000",
        "hotsoon_filtered_count": "0",
        "hotsoon_has_more": "0",
        "follower_count": "0",
        "is_familiar": "0",
        "page_source": "0",
        "manifest_version_code": "110501",
        "_rticket": _rticket,
        "app_type": "normal",
        "iid": iid,
        "channel": "gdt_growth14_big_yybwz",
        "device_type": "21091116AC",
        "language": "zh",
        "cpu_support64": "true",
        "host_abi": "armeabi-v7a",
        "resolution": "1080*2260",
        "openudid": openudid,
        "update_version_code": "11509900",
        "cdid": cdid,
        "os_api": "31",
        "mac_address": mac_address,
        "dpi": "440",
        "oaid": "",  # 705a52036f49ecc7(设备虚拟ID), 可以为空
        "ac": "wifi",
        "device_id": device_id,
        "mcc_mnc": "46001",
        "os_version": "12",
        "version_code": "110500",
        "app_name": "aweme",
        "version_name": "11.5.0",
        "device_brand": "Redmi",
        "ssmix": "a",
        "device_platform": "android",
        "aid": "1128",
        "ts": ts
    }

    param_string = urlencode(param_dict)
    print("拼接后的URL参数=>", param_string)

    # 获取评论时，有cookie
    # cookie_string = "install_id={}; ttreq={}; odin_tt={}".format(iid, ttreq, odin_tt)
    cookie_string = None
    gorgon, khronos = get_gorgon(script, param_string, cookie_string)

    resp = requests.get(
        url="https://api5-normal-c-lq.amemv.com/aweme/v2/comment/list/",
        params=param_dict,
        headers={
            "user-agent": "com.ss.android.ugc.aweme/110501 (Linux; U; Android 12; zh_CN; 21091116AC; Build/SP1A.210812.016; Cronet/TTNetVersion:3c28619c 2020-05-19 QuicVersion:0144d358 2020-03-24)",
            "x-khronos": str(khronos),
            "x-gorgon": gorgon
        },
        cookies={
            "install_id": iid,
            "odin_tt": odin_tt
        }
    )
    print("\n-----------获取评论-------------\n")
    print(resp.text)


if __name__ == '__main__':
    get_comment_list()
