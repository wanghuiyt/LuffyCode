import hashlib

import frida
import time

rdev = frida.get_remote_device()
session = rdev.attach("抖音短视频")

scr = """
rpc.exports = {
    execandleviathan: function(i2, str){
        var result;
        Java.perform(function(){
            // 字符串->js字节->java字节
            
            // 先处理拼接好的数据（字节数组）
            var bArr = [];
            for(var i=0;i<str.length;i+=2){
                var item = (parseInt(str[i],16) << 4) + parseInt(str[i+1],16);
                bArr.push(item);
            }
            
            // 转换为Java字节数组
            var dataByteArray = Java.array('byte', bArr);
            
            // 调用leviathan方法
            var Gorgon = Java.use("com.ss.sys.ces.a");
            result = Gorgon.leviathan(-1, i2, dataByteArray);
        });
        return result;
    }
}
"""

script = session.create_script(scr)
script.load()

khronos = int(time.time())

obj = hashlib.md5()
obj.update(str(khronos).encode("utf-8"))
random_str = obj.hexdigest()

un_sign_str = f"{random_str}000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
sign_byte_list = script.exports.execandleviathan(khronos, un_sign_str)
print(sign_byte_list)

data_list = []
for item in sign_byte_list:
    if item < 0:
        item += 256
    data_list.append("%02x" % item)

print("".join(data_list))
