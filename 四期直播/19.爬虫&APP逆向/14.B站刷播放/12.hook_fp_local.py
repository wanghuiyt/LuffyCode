import sys
import frida

rdev = frida.get_remote_device()
session = rdev.attach("哔哩哔哩")

scr = """
Java.perform(function () {
    var a = Java.use("com.bilibili.lib.biliid.internal.fingerprint.a.a");
    var i = Java.use("kotlin.g0.i");
    
    a.e.implementation = function(str){
        console.log("第一个参数：",str);
        var res = this.e(str);
        console.log("res:",res);
        return res;
    }
    
    a.b.implementation = function(str){
        console.log("b参数=>",str);
        var res = this.b(str);
        console.log("b返回值=>",res);
        return res;
    }
    
    // g
    i.g.implementation = function(){
        var res = this.g();
        console.log("生成的值=>g=",res);
        return res;
    }
    
    // h
    i.h.implementation = function(){
        var res = this.h();
        console.log("生成的值=>h=",res);
        return res;
    }
    
    // i
    i.i.implementation = function(){
        var res = this.i();
        console.log("生成的值=>2=",res);
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

# 第一个参数： XX8A435834E141A46A111E6DEDD4D97D68E09 21091116AC MOLY.NR15.R3.MP.V29.5.P59,MOLY.NR15.R3.MP.V29.5.P59
# res: 32,91,-83,19,-112,63,21,125,21,-121,-108,-112,106,-13,-114,-74

# b参数=> 205bad13903f157d158794906af38eb620220910125022820181316256436c
# 生成的值=>g= 0
# 生成的值=>h= 60
# 生成的值=>i2= 2
# b返回值=> 78
