import sys
import frida

rdev = frida.get_remote_device()
session = rdev.attach("哔哩哔哩")

scr = """
Java.perform(function() {
    var a = Java.use("com.bilibili.api.a");

    a.o.implementation = function(bVal){
        console.log("谁生成调用getSessionId的类，",bVal);
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
        this.o(bVal);
    }

});
"""

script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)
script.load()
sys.stdin.read()

# java.lang.Throwable
# 	at com.bilibili.api.a.o(Native Method)
# 	at tv.danmaku.bili.utils.p.b(BL:1)
# 	at tv.danmaku.bili.proc.MainBiliAppProc.v(BL:2)
# 	at tv.danmaku.bili.proc.k.invoke(Unknown Source:2)
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
