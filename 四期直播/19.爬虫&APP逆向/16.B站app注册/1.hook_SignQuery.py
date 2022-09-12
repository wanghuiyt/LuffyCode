import sys
import frida
from frida.core import Device

rdev = frida.get_remote_device()
session = rdev.attach("哔哩哔哩")


scr = """
Java.perform(function(){
    var SignedQuery = Java.use("com.bilibili.nativelibrary.SignedQuery");
    
    // 构造方法 $init
    SignedQuery.$init.implementation = function(v1,v2){
        console.log(v1 + "--" + v2);
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
        this.$init(v1,v2);
    }
});
"""

script = session.create_script(scr)

script.load()
sys.stdin.read()

# appkey=bca7e84c2d947ac6&build=6240300&c_locale=zh_CN&channel=xxl_gdt_wm_253&cid=1&mobi_app=android&platform=android&s_locale=zh_CN&tel=7828099329&ts=1662903380--aacbe7b8ca56ac9d63498a11a0f39433
# java.lang.Throwable
# 	at com.bilibili.nativelibrary.SignedQuery.<init>(Native Method)
# 	at com.bilibili.nativelibrary.LibBili.so(Native Method)
# 	at com.bilibili.nativelibrary.LibBili.h(BL:3)
# 	at com.bilibili.lib.accounts.a.h(BL:4)
# 	at com.bilibili.okretro.f.a.c(BL:14)
# 	at com.bilibili.okretro.f.a.a(BL:6)
# 	at com.bilibili.okretro.d.a.execute(BL:24)
# 	at com.bilibili.lib.accounts.BiliPassportApi.s(BL:3)
# 	at com.bilibili.lib.accounts.b.S(BL:1)
# 	at com.bilibili.lib.accountsui.p.d$o.a(BL:3)
# 	at com.bilibili.lib.accountsui.p.d$o.call(BL:1)
# 	at bolts.h$j.run(BL:3)
# 	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1167)
# 	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:641)
# 	at java.lang.Thread.run(Thread.java:920)
