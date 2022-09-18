import sys
import frida

rdev = frida.get_remote_device()
session = rdev.attach("抖音短视频")

scr = """
Java.perform(function(){
     var AppLog = Java.use("com.ss.android.common.applog.AppLog");
     
     AppLog.getLogEncryptSwitch.implementation = function(){
        var res = this.getLogEncryptSwitch();
        console.log("res=>",res);
        return false;
     }
     
     // hook getDefault
     var NetworkClient = Java.use("com.bytedance.common.utility.NetworkClient");
     
     NetworkClient.getDefault.implementation = function(){
        var res = this.getDefault();
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
        return res;
     }
})
"""

script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)
script.load()
sys.stdin.read()
