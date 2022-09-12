import sys
import frida

rdev = frida.get_remote_device()
session = rdev.attach("哔哩哔哩")

scr = """
Java.perform(function(){
    var h = Java.use("tv.danmaku.biliplayerimpl.report.heartbeat.h");
    var a = Java.use("com.bilibili.commons.m.a");
    
    // 获取session
    h.t2.implementation = function(str){
        console.log("设置session=>",str);
        this.t2(str);
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
    }
    
    // Sha1加密
    a.i.implementation = function(str){
        console.log("加密前=>", str);
        var res = this.i(str);
        console.log("加密后=>", res);
        return res;
    }
});
"""

script = session.create_script(scr)

script.load()
sys.stdin.read()


# sha1加密
# 加密前=> 1662872323022428526
# 加密后=> 3bae4f01e508abff81e4e54a52deb8bcd73a4828
# 加密前=> 1662872323492952018
# 加密后=> 3b3ee02af2747898f803447ba0eb91bb63b65afb

# session
# 设置session=> 96eb2fbc1cfd306b5db82eeacac4adc8ef6d8762
# java.lang.Throwable
# 	at tv.danmaku.biliplayerimpl.report.heartbeat.h.t2(Native Method)
# 	at tv.danmaku.biliplayerimpl.report.heartbeat.h$a.b(BL:5)
# 	at tv.danmaku.biliplayerimpl.report.heartbeat.d.L7(BL:2)
# 	at tv.danmaku.biliplayerimpl.report.heartbeat.d.u7(BL:3)
# 	at tv.danmaku.biliplayerimpl.core.PlayerCoreServiceV2$l.onPrepared(BL:2)
# 	at t3.a.i.b.i$j.onPrepared(BL:6)
# 	at tv.danmaku.ijk.media.player.AbstractMediaPlayer.notifyOnPrepared(BL:2)
# 	at tv.danmaku.ijk.media.player.IjkMediaPlayer$EventHandler.handleMessage(BL:107)
# 	at android.os.Handler.dispatchMessage(Handler.java:106)
# 	at android.os.Looper.loopOnce(Looper.java:210)
# 	at android.os.Looper.loop(Looper.java:299)
# 	at android.app.ActivityThread.main(ActivityThread.java:8302)
# 	at java.lang.reflect.Method.invoke(Native Method)
# 	at com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run(RuntimeInit.java:576)
# 	at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:1073)




