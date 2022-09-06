import sys
import frida

# 连接手机
rdev = frida.get_remote_device()

# Hook手机上的哪个APP(app的包名字)
# session = rdev.attach("com.che168.autotradercloud")  # 车智赢+ 或 进程ID
session = rdev.attach("得物(毒)")

scr = """
Java.perform(function () {
    // 包.类
    var Builder = Java.use("okhttp3.OkHttpClient$Builder");
    
    Builder.proxy.implementation = function(proxy){
        var res = this.proxy(null);
        return res;
    }
    
});
"""

script = session.create_script(scr)
script.load()
sys.stdin.read()
