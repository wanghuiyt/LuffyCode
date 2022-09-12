import sys
import frida

rdev = frida.get_remote_device()
session = rdev.attach("哔哩哔哩")

scr = """
Java.perform(function() {
    var a = Java.use("com.bilibili.lib.biliid.utils.f.a");
    
    a.f.implementation = function(context){
        console.log("f参数=",context);
        var res = this.f(context);
        console.log("生成的did:", res);
        return res;
    }
    
    a.c.implementation = function(context){
        console.log("参数：", context);
        var res = this.c(context);
        console.log("生成的did=",res);
        return res;
    }
    
    // 获取最终did的值
    a.b.implementation = function(str){
        console.log("B参数：",str);
        var res = this.b(str);
        console.log("最终did的值为：",res);
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

# 参数： BiliApplication(tv.danmaku.bili)@7cb5f56
# f参数= BiliApplication(tv.danmaku.bili)@7cb5f56
# 生成的did: |||
# 生成的did= Lhp8SitJf0dwR3ZAc0JySws5CDgBMAEwBkcE

# 生成的did: |||
# B参数： 54f6ab6877163109@21091116AC
# 最终did的值为： Lhp8SitJf0dwR3ZAc0JySws5CDgBMAEwBkcE
