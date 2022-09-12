import sys
import frida

rdev = frida.get_remote_device()
session = rdev.attach("哔哩哔哩")


scr = """
Java.perform(function(){
    var Pair = Java.use("kotlin.Pair");
    
    Pair.$init.implementation = function(v1,v2){
        console.log("构造方法=>", v1 + "--" + v2);
        this.$init(v1,v2);
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
    }
    
    Pair.component2.implementation = function(){
        var res = this.component2();
        console.log("device_meta=>",res);
        return res;
    }
    
    Pair.component1.implementation = function(){
        var res = this.component1();
        console.log("dt=>",res);
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



