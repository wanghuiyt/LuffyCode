import sys
import frida

rdev = frida.get_remote_device()
session = rdev.attach("得物(毒)")

scr = """
Java.perform(function(){
    var RequestUtils = Java.use("com.shizhuang.duapp.common.utils.RequestUtils");
    var AESEncrypt = Java.use("com.duapp.aesjni.AESEncrypt");
    
    RequestUtils.a.overload('java.util.Map', 'long').implementation = function(map, j){
        var res = this.a(map, j);
        console.log("a--->newSign=",res);
        return res;
    }
    
    RequestUtils.b.overload('java.util.Map', 'long').implementation = function(map, j){
        var res = this.b(map, j);
        console.log("b--->newSign=",res);
        return res;
    }
    
    RequestUtils.c.overload('java.util.Map', 'long').implementation = function(map, j){
        // 输出字典
        var Map = Java.use('java.util.HashMap');
        var obj = Java.cast(map, Map);
        console.log("字典的值为：", obj.toString());
        
        var res = this.c(map, j);
        console.log("c--->newSign=",res);
        return res;
    }
    
    AESEncrypt.encode.overload('java.lang.Object','java.lang.String').implementation = function(obj,str){
        console.log("str-->",str);
        var res = this.encode(obj,str);
        console.log("res-->",res);
        return res;
    }
    
    AESEncrypt.encodeByte.overload('[B','java.lang.String').implementation = function(obj,str){
        console.log("===>",str);
        var res = this.encodeByte(obj,str);
        console.log("===>",res);
        return res;
    }
});
"""

script = session.create_script(scr)
script.load()
sys.stdin.read()
