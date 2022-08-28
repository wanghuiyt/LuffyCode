import requests
import time
import execjs
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json


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


def aes_encrypt(data_string, key, iv):
    key = binascii.a2b_hex(key)
    iv = binascii.a2b_hex(iv)
    aes = AES.new(key=key, mode=AES.MODE_CBC, IV=iv)
    raw = pad(data_string.encode("utf-8"), 16)
    aes_bytes = aes.encrypt(raw)
    return binascii.b2a_hex(aes_bytes).decode()



guid = JS.call("createGuid")
pid = JS.call("createGuid")
flow_id = pid
platform = "4330701"
app_ver = "1.2.10"
vid = "i000075mu8r"
ctime = str(int(time.time()))
ending = "https://w.yangshipin.cn/|mozilla/5.0 (windows nt ||Mozilla|Netscape|Win32|"
data_list = ["", vid, ctime, "mg3c3b04ba", app_ver, guid, platform, ending]
data_string = "|".join(data_list)
qn = JS.call("createQn", data_string)
encrypt_string = f"|{qn}{data_string}"
es = aes_encrypt(encrypt_string, "4E2918885FD98109869D14E0231A0BF4", "16B17E519DDD0CE5B79D7A63A4DD801C").upper()
ckey = f"--01{es}"
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

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "referer": "https://w.yangshipin.cn/"
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

url = info_dict["vl"]["vi"][0]["ul"]["ui"][0]["url"]
vkey = info_dict["vl"]["vi"][0]["fvkey"]
fn = info_dict["vl"]['vi'][0]["fn"]
vurl = f"{url}{fn}?sdtfrom={platform}&guid={guid}&vkey={vkey}&platform=2"
print(vurl)



