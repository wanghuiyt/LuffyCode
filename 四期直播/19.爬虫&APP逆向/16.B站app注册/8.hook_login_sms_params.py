import sys
import frida

rdev = frida.get_remote_device()
session = rdev.attach("哔哩哔哩")

scr = """
Java.perform(function(){
    var a = Java.use("com.bilibili.okretro.f.a");
    
    a.c.implementation = function(uVar,c0Var,aVar){
        this.c(uVar,c0Var,aVar);
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
    }
});
"""

script = session.create_script(scr)
script.load()
sys.stdin.read()

# java.lang.Throwable
# 	at com.bilibili.okretro.f.a.c(Native Method)
# 	at com.bilibili.okretro.f.a.a(BL:6)
# 	at com.bilibili.okretro.d.a.execute(BL:24)
# 	at com.bilibili.lib.accounts.BiliPassportApi.l(BL:6)
# 	at com.bilibili.lib.accounts.b.A(BL:1)
# 	at com.bilibili.lib.accountsui.p.d$k.a(BL:11)
# 	at com.bilibili.lib.accountsui.p.d$k.call(BL:1)
# 	at bolts.h$j.run(BL:3)
# 	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1167)
# 	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:641)
# 	at java.lang.Thread.run(Thread.java:920)

