import gzip
import random
import time
import uuid
import requests
from hashlib import md5

import dy_gorgon2
from urllib.parse import quote_plus


def create_random_mac(sep=":"):
    data_list = []
    for i in range(1, 7):
        part = "".join(random.sample("0123456789ABCDEF", 2))
        data_list.append(part)
    return sep.join(data_list)


def create_uuid():
    return str(uuid.uuid4())


def create_openudid():
    while True:
        value = "".join([hex(random.randint(1, 255))[2:] for _ in range(10)])
        if len(value) > 13:
            return value


def md5_encrypt(data_bytes, isUpper=False):
    obj = md5()
    obj.update(data_bytes)
    if isUpper:
        return obj.hexdigest().upper()
    return obj.hexdigest()


def run():
    _rticket = int(time.time() * 1000)
    mac_address = create_random_mac()
    device_type = "21091116AC"
    cdid = create_uuid()
    openudid = create_openudid()
    oaid = ""
    ts = int(time.time())
    _rticket2 = int(time.time() * 1000)

    param_str = f"ac=wifi&mac_address={mac_address}&channel=gdt_growth14_big_yybwz&aid=1128&app_name=aweme&version_code=110500&version_name=11.5.0&device_platform=android&ssmix=a&device_type={device_type}&device_brand=Redmi&language=zh&os_api=31&os_version=12&openudid={openudid}&manifest_version_code=110501&resolution=1080*2260&dpi=440&update_version_code=11509900&_rticket={_rticket}&mcc_mnc=46001&cpu_support64=true&host_abi=armeabi-v7a&app_type=normal&ts={ts}&cdid={cdid}&oaid={oaid}&manifest_version_code=110501&_rticket={_rticket2}&app_type=normal&channel=gdt_growth14_big_yybwz&device_type={device_type}&language=zh&cpu_support64=true&host_abi=armeabi-v7a&resolution=1080*2260&openudid={openudid}&update_version_code=11509900&cdid={cdid}&os_api=31&mac_address={mac_address}&dpi=440&oaid={oaid}&ac=wifi&mcc_mnc=46001&os_version=12&version_code=110500&app_name=aweme&version_name=11.5.0&device_brand=Redmi&ssmix=a&device_platform=android&aid=1128&ts={ts}"

    data_string = param_str.format(
        mac_address=quote_plus(mac_address),
        device_type=device_type,
        openudid=openudid,
        _rticket=_rticket,
        ts=ts,
        cdid=cdid,
        oaid=oaid,
        _rticket2=_rticket2,
    )

    print(data_string)

    body_dict = {
        "device_model": device_type,
        "release_build": "b44f245_20200615_{}".format(create_uuid()),
        # "release_build": "b44f245_20200615_436d6cbc-aecc-11ea-bfa1-02420a000026",
        "mc": mac_address,
        "cdid": cdid,
        "sig_hash": "aea615ab910015038f73c47e45d21466",
        # "google_aid": "",
        "openudid": openudid,
        "clientudid": create_uuid(),
        "xreg": create_uuid(),
        "xreg2": create_uuid(),
        "time": int(time.time() * 1000),
        "apk_first_install_time": int(time.time() * 1000) - 100000,
        "is_system_app": 1,
        "_gen_time": int(time.time() * 1000),
    }

    body_string = '{"magic_tag":"ss_app_log","header":{"display_name":"抖音短视频","update_version_code":11509900,"manifest_version_code":110501,"app_version_minor":"","aid":1128,"channel":"gdt_growth14_big_yybwz","appkey":"57bfa27c67e58e7d920028d3","package":"com.ss.android.ugc.aweme","app_version":"11.5.0","version_code":110500,"sdk_version":"2.14.0-alpha.4","sdk_target_version":29,"git_hash":"c1aa4085","os":"Android","os_version":"12","os_api":31,"device_model":"%(device_model)s","device_brand":"Redmi","device_manufacturer":"Xiaomi","cpu_abi":"armeabi-v7a","release_build":"%(release_build)s","density_dpi":440,"display_density":"mdpi","resolution":"2260x1080","language":"zh","mc":"%(mc)s","timezone":8,"access":"wifi","not_request_sender":0,"carrier":"小米移动","mcc_mnc":"46001","rom":"MIUI-V13.0.6.0.SGBCNXM","rom_version":"miui_V130_V13.0.6.0.SGBCNXM","cdid":"%(cdid)s","sig_hash":"%(sig_hash)s","openudid":"%(openudid)s","clientudid":"%(clientudid)s","sim_serial_number":[],"region":"CN","tz_name":"Asia\/Shanghai","tz_offset":28800,"sim_region":"cn","oaid":{"req_id":"%(xreg)s","hw_id_version_code":"null","take_ms":"20","is_track_limited":"null","query_times":"1","id":"","time":"%(time)s"},"oaid_may_support":true,"req_id":"%(xreg2)s","custom":{"filter_warn":0,"web_ua":"Mozilla\/5.0 (Linux; Android 12; 21091116AC Build\/SP1A.210812.016; wv) AppleWebKit\/537.36 (KHTML, like Gecko) Version\/4.0 Chrome\/99.0.4844.88 Mobile Safari\/537.36"},"pre_installed_channel":"ame_xiaomi2020_1311_yz1","apk_first_install_time":%(apk_first_install_time)s,"is_system_app":0,"sdk_flavor":"china"},"_gen_time":%(_gen_time)s}'

    body_str = body_string % body_dict

    # 请求体gzip压缩
    gzip_body = gzip.compress(body_str.encode("utf-8"))
    bs = bytearray(gzip_body)
    bs[3: 10] = [0, 0, 0, 0, 0, 0, 0]
    v1 = [i - 256 if i > 127 else i for i in bs]

    # ttEncrypt加密
    ttencrypt_bytes_list = dy_gorgon2.get_ttencrypt(list(v1), len(v1))

    # 得到最终要发送的请求体数据
    ttencrypt_bytes = bytearray([i + 256 if i < 0 else i for i in ttencrypt_bytes_list])

    # 生成x-ss-stud
    x_ss_stud = md5_encrypt(bytes(ttencrypt_bytes), True)

    # 第一段 C
    c = md5_encrypt(data_string.encode("utf-8"))

    # 第二段 请求中的X-SS-STUD 如果是GET请求，则是 00000000000000000000000000000000
    str3 = x_ss_stud

    # 第三段 cookie MD5值
    str4 = "00000000000000000000000000000000"

    # 第四段 session_id MD5值
    str5 = "00000000000000000000000000000000"

    un_sign_string = f"{c}{str3}{str4}{str5}"
    khronos = int(time.time())
    gorgon_byte_list = dy_gorgon2.execandleviathan(khronos, un_sign_string)
    gorgon = dy_gorgon2.m44417a(gorgon_byte_list)

    res = requests.post(
        url="https://ib.snssdk.com/service/2/device_register/?{}".format(data_string),
        data=ttencrypt_bytes,
        headers={
            "x-ss-stub": x_ss_stud,
            "content-encoding": "gzip",
            "x-ss-req-ticket": str(khronos),
            "x-khronos": str(khronos),
            "x-gorgon": gorgon,
            "content-type": "application/octet-stream;tt-data=a",
            "user-agent": "com.ss.android.ugc.aweme/110501 (Linux; U; Android 12; zh_CN; 21091116AC; Build/SP1A.210812.016; Cronet/TTNetVersion:3c28619c 2020-05-19 QuicVersion:0144d358 2020-03-24)"
        }
    )
    res_json = res.json()
    print(res_json)

    # ttreq = res.cookies.get_dict()['ttreq']
    # install_id_str = res_json['install_id_str']
    # device_token = res_json['device_token']
    # device_id = res_json['device_id']
    # print(device_id, install_id_str)


if __name__ == '__main__':
    run()
