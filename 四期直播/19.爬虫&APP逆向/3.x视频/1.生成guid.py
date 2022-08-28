import execjs

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
# guid = JS.call("createGuid")
# pid = JS.call("createGuid")
vn = "|i000075mu8r|1661676601|mg3c3b04ba|1.2.10|l7d2qjtv_kf3lb8sg59q|4330701|https://w.yangshipin.cn/|mozilla/5.0 (windows nt ||Mozilla|Netscape|Win32|"
qn = JS.call("createQn", vn)
# print(guid)
# print(pid)
print(qn)

