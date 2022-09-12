import sys
import frida

rdev = frida.get_remote_device()
session = rdev.attach("哔哩哔哩")

scr = """
Java.perform(function() {
    var c = Java.use("com.bilibili.api.c");

    c.b.implementation = function(str){
        console.log("buvid=",str);
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
        this.b(str);
    }

});
"""

script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)
script.load()
sys.stdin.read()

# buvid= XX8A435834E141A46A111E6DEDD4D97D68E09
# java.lang.Throwable
# 	at com.bilibili.api.c.b(Native Method)
# 	at c2.f.b0.c.a.d.e(BL:1)
# 	at c2.f.b0.c.a.d.a(BL:11)
# 	at tv.danmaku.bili.utils.BiliInitHelper$initConfig$2.invoke(BL:1)
# 	at tv.danmaku.bili.utils.BiliInitHelper$initConfig$2.invoke(Unknown Source:0)
# 	at com.bilibili.lib.blconfig.internal.CommonContext.c(BL:1)
# 	at com.bilibili.lib.blconfig.internal.DecisionTree.c(BL:17)
# 	at com.bilibili.lib.blconfig.internal.DecisionTree.d(BL:1)
# 	at com.bilibili.lib.blconfig.internal.DecisionTree.c(BL:23)
# 	at com.bilibili.lib.blconfig.internal.ABNode$toFunction$1$whiteFunc$2.invoke(BL:2)
# 	at com.bilibili.lib.blconfig.internal.ABNode$toFunction$1$whiteFunc$2.invoke(BL:1)
# 	at kotlin.SynchronizedLazyImpl.getValue(BL:6)
# 	at com.bilibili.lib.blconfig.internal.ABNode$toFunction$1.a(Unknown Source:7)
# 	at com.bilibili.lib.blconfig.internal.ABNode$toFunction$1.b(BL:2)
# 	at com.bilibili.lib.blconfig.internal.ABNode$toFunction$1.invoke(BL:1)
# 	at com.bilibili.lib.blconfig.internal.ABSource.f(BL:7)
# 	at com.bilibili.lib.blconfig.internal.ABSource.invoke(BL:1)
# 	at com.bilibili.lib.blconfig.internal.h.get(BL:1)
# 	at com.bilibili.lib.blconfig.a$a.a(BL:1)
# 	at tv.danmaku.bili.httpdns.internal.configs.a.c(BL:1)
# 	at tv.danmaku.bili.h0.a.b.a.a.b(BL:1)
# 	at tv.danmaku.bili.h0.a.b.a.a.g(BL:1)
# 	at tv.danmaku.bili.h0.a.a.b(BL:1)
# 	at tv.danmaku.bili.b0.b.a(BL:2)
# 	at tv.danmaku.bili.proc.MainBiliAppProc.a(BL:8)
# 	at tv.danmaku.bili.proc.MainBiliAppProcWrapper$onApplicationCreate$1.invoke(BL:2)
# 	at tv.danmaku.bili.proc.MainBiliAppProcWrapper$onApplicationCreate$1.invoke(BL:1)
# 	at tv.danmaku.bili.delaytask.a.l(BL:3)
# 	at tv.danmaku.bili.delaytask.a.e(BL:2)
# 	at com.bilibili.base.util.a.e(BL:1)
# 	at tv.danmaku.bili.ui.main2.userprotocol.e.onClick(BL:4)
# 	at android.view.View.performClick(View.java:7758)
# 	at android.view.View.performClickInternal(View.java:7731)
# 	at android.view.View.access$3700(View.java:862)
# 	at android.view.View$PerformClick.run(View.java:29348)
# 	at android.os.Handler.handleCallback(Handler.java:938)
# 	at android.os.Handler.dispatchMessage(Handler.java:99)
# 	at android.os.Looper.loopOnce(Looper.java:210)
# 	at android.os.Looper.loop(Looper.java:299)
# 	at android.app.ActivityThread.main(ActivityThread.java:8302)
# 	at java.lang.reflect.Method.invoke(Native Method)
# 	at com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run(RuntimeInit.java:576)
# 	at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:1073)