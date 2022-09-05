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
    var AHAPIHelper = Java.use("com.autohome.ahkit.AHAPIHelper");  // 这里不是真正的Sign计算
    var SignManager = Java.use("com.che168.atclibrary.base.SignManager");
    var CheckSignUtil = Java.use("com.autohome.ahkit.jni.CheckSignUtil");
    
    // 密码，Hook，替换
    //UserModel.loginByPassword.implementation = function(str,str2,str3,callback){
    //    console.log(str,str2,str3);
    //    
    //    // 执行原来的方法
    //    this.loginByPassword(str,str2,str3,callback);
    //}
    
    // MD5，Hook，替换
    // SecurityUtil.encodeMD5.implementation = function(str){
    //     console.log("明文=",str);
    //     var res = this.encodeMD5(str);
    //     console.log("密文=",res);
    //     return res;
    // }
    
    // 3Des，hook
    SecurityUtil.encode3Des.implementation = function(context, str){
        console.log("请求参数：", str);
        var res = this.encode3Des(context, str);
        console.log("3des: ", res);
        return res;
    }
    
    // 3Des key， hook
    CheckSignUtil.get3desKey.implementation = function(context){
        var res = this.get3desKey(context);
        console.log("key：", res);
        return res;
    }
    
    // Sign，Hook，替换
    AHAPIHelper.toSign.implementation = function(context, treeMap){
        // 执行原来的方法
        var res = this.toSign(context, treeMap);
        console.log("Sign签名：", res);
        return res;
    }
    
    // Sign
    SignManager.signByType.implementation = function(i, treeMap){
        console.log("参数：", treeMap);
        var res = this.signByType(i, treeMap);
        console.log("计算Sign：",res);
        return res;
    }
});
"""

script = session.create_script(scr)
script.load()
sys.stdin.read()
