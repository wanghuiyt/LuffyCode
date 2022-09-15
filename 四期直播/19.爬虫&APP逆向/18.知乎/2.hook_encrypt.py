import sys
import frida

rdev = frida.get_remote_device()
session = rdev.attach("知乎")

scr = """
Java.perform(function(){
    var CloudIDHelper = Java.use("com.zhihu.android.cloudid.CloudIDHelper");
    
    CloudIDHelper.encrypt.implementation = function(str,str2,str3,str4,str5,str6,str7){
        console.log("str=>", str);
        console.log("str2=>", str2);
        console.log("str3=>", str3);
        console.log("str4=>", str4);
        console.log("str5=>", str5);
        console.log("str6=>", str6);
        console.log("str7=>", str7);
        var res = this.encrypt(str,str2,str3,str4,str5,str6,str7);
        console.log("res=>", res);
    }
});
"""

script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)
script.load()
sys.stdin.read()
