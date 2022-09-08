import sys
import frida

rdev = frida.get_remote_device()
session = rdev.attach("哔哩哔哩")

scr = """
Java.perform(function () {
    var b = Java.use("t3.a.i.a.a.a.b");
    
    b.b.implementation = function(str){
        console.log("传入参数：", str);
        var res = this.b(str);
        console.log("sha256加密后=",res);
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
