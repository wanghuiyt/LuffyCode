import requests
import time
import json
from urllib.parse import urljoin
from utils import get_distance
from utils import get_slide_track
from utils import turn_img_back
import execjs
import io
from hashlib import md5


def rsa_encrpt(text, pub_key, md):
    """
    rsa 加密
    :param text: 文本
    :param pub_key: 公钥
    :param md: 加密系数
    :return:
    """
    import rsa
    pubkey = rsa.PublicKey(int(md, 16), int(pub_key, 16))  # rsa库公钥形式
    rs = rsa.encrypt(text.encode(), pubkey)
    return rs.hex()


def handler(challenge, gt, proxy_dict=None):
    session = requests.session()
    session.proxies = proxy_dict
    session.headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }

    t = str(int(time.time() * 1000))
    resp = session.get(f"https://www.geetest.com/demo/gt/register-slide?t={t}")
    challenge = resp.json()['challenge']
    gt = resp.json()['gt']

    # challenge = "d067f072e52142864ea78b323b8b2855"
    # gt = "1c0ea7c7d47d8126dda19ee3431a5f38"

    session.get(f"https://api.geetest.com/gettype.php?gt={gt}&callback=geetest_{t}")
    t = str(int(time.time() * 1000))
    get_php_url = f"https://api.geetest.com/ajax.php?gt={gt}&challenge={challenge}&lang=zh-cn&pt=0&client_type=h5&w="
    get_php_resp = session.get(get_php_url)

    t = str(int(time.time() * 1000))
    get_php_url = f"https://api.geetest.com/get.php?is_next=true&type=slide3&gt={gt}&challenge={challenge}&lang=zh-cn&https=true&protocol=https%3A%2F%2F&offline=false&product=popup&api_server=api.geetest.com&isPC=true&autoReset=true&width=100%25&callback=geetest_{t}"
    get_php_resp = session.get(get_php_url)
    get_json_str = get_php_resp.text.replace(f"geetest_{t}(", "").rstrip(")")
    get_dict = json.loads(get_json_str)

    id = get_dict['id']
    challenge = get_dict['challenge']
    gt = get_dict['gt']
    bg = get_dict['bg']

    c = get_dict['c']
    s = get_dict['s']

    fullbg = get_dict['fullbg']
    slice = get_dict['slice']
    static_servers = "https://" + get_dict['static_servers'][0]

    bg_url = urljoin(static_servers, bg)
    fullbg_url = urljoin(static_servers, fullbg)
    slice_url = urljoin(static_servers, slice)

    bg_object = io.BytesIO()
    with io.BytesIO() as f1:
        resp = session.get(bg_url)
        f1.write(resp.content)
        turn_img_back(f1, bg_object)

    slice_object = io.BytesIO()
    resp = session.get(slice_url)
    slice_object.write(resp.content)

    x = get_distance(
        bg=bg_object.getvalue(),
        tp=slice_object.getvalue(),
        im_show=False
    )

    gui = get_slide_track(x)
    # print(gui)
    # # print(gui[-1][-1])
    all_t = gui[-1][-1]
    # print(gui)
    # print(all_t)

    f = open("finally.js", mode="r", encoding="utf-8")
    js_source = f.read()
    f.close()
    obj = execjs.compile(js_source)

    l = obj.call("one", gui, c, s)

    # // 第一个参数: 横向滑动距离
    # // 第二个参数: 加密后的轨迹
    # // 第三个参数: 滑动持续时间
    # // 第四个参数: 上一次get.php获取到的所有东西
    o = obj.call("second", x, l, all_t, challenge)

    # // o['rp'] = U(i['gt'] + '341ae4def027d6e1b391d29210c5c0faai'['slice'](0, 32) + o['passtime']);
    md5_obj = md5()
    ready_s = gt + challenge[:32] + str(o['passtime'])

    md5_obj.update(ready_s.encode("utf-8"))
    o['rp'] = md5_obj.hexdigest()

    # 获取aeskey
    aeskey = obj.call("create_aeskey")

    # aeskey = "c9ac3341fe02ef65"
    # 对aeskey进行加密
    p = '00C1E3934D1614465B33053E7F48EE4EC87B14B95EF88947713D25EECBFF7E74C7977D02DC1D9451F79DD5D1C10C29ACB6A9B4D6FB7D0A0279B6719E1772565F09AF627715919221AEF91899CAE08C0D686D748B20A3603BE2318CA6BC2B59706592A9219D0BF05C9F65023A21D2330807252AE0066D59CEEFA5F2748EA80BAB81'
    q = '10001'

    r = rsa_encrpt(aeskey, q, p)

    rr = obj.call("third", o, aeskey, r)

    rr['gt'] = gt
    rr['challenge'] = challenge

    callback_string = rr['callback'] = f"geetest_{int(time.time() * 1000)}"
    finally_resp = session.get("https://api.geetest.com/ajax.php", params=rr)
    return json.loads(finally_resp.text.strip(callback_string).strip("(").strip(")"))


def do_geetest():
    # 注册. 获取第一步信息.
    resp = requests.get(f"https://www.geetest.com/demo/gt/register-slide")
    challenge = resp.json()['challenge']
    gt = resp.json()['gt']

    res_dict = handler(challenge, gt)
    print(res_dict)


if __name__ == '__main__':
    do_geetest()
