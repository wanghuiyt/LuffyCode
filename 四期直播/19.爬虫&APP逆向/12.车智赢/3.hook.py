import sys
import frida

# 连接手机
rdev = frida.get_remote_device()

# Hook手机上的哪个APP(app的包名字)
# session = rdev.attach("com.che168.autotradercloud")  # 车智赢+ 或 进程ID
session = rdev.attach("车智赢+")

scr = """
Java.perform(function () {
    // 包.类
    var UserModel = Java.use("com.che168.autotradercloud.user.model.UserModel");
    var SecurityUtil = Java.use("com.autohome.ahkit.utils.SecurityUtil");
    
    // Hook，替换
    UserModel.loginByPassword.implementation = function(str,str2,str3,callback){
        console.log(str,str2,str3);
        
        // 执行原来的方法
        this.loginByPassword(str,str2,str3,callback);
    }
    
    // MD5，Hook，替换
    SecurityUtil.encodeMD5.implementation = function(str){
        console.loe("明文=",str);
        var res = this.encodeMD5(str);
        console.loe("密文=",res);
        return res;
    }
});
"""

script = session.create_script(scr)
script.load()
sys.stdin.read()
