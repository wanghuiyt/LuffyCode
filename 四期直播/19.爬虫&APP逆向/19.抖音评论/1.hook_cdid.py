import sys
import frida

rdev = frida.get_remote_device()
session = rdev.attach("抖音短视频")

scr = """
Java.perform(function(){
    var cls = Java.use("com.ss.android.deviceregister.d.a$1");
    
    cls.a.implementation = function(arg4){
        var res = this.a(arg4);
        console.log("res=>",res);
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
        return res;
    }
});
"""

script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)
script.load()
sys.stdin.read()

