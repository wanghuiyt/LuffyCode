import frida

rdev = frida.get_remote_device()
session = rdev.attach("抖音短视频")

scr = """
var result;
function leviathan(i2, str){
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
};

function ttEncrypt(bArr, i){
    Java.perform(function(){
        // 转换为Java数组
        var dataByteArray = Java.array('byte', bArr);
        
        // 调用ttEncrypt方法
        var EncryptorUtil = Java.use("com.bytedance.frameworks.encryptor.EncryptorUtil");
        result = EncryptorUtil.ttEncrypt(dataByteArray, i);
    });
    return result;
};

rpc.exports = {
    leviathan: leviathan,
    ttencrypt: ttEncrypt
}
"""

script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)
script.load()


def execandleviathan(i2, s):
    return script.exports.leviathan(i2, s)


def get_ttencrypt(v1, v1_length):
    return script.exports.ttencrypt(v1, v1_length)


def m44417a(barr):
    data_list = []
    for item in barr:
        if item < 0:
            item += 256
        data_list.append("%02x" % item)
    return "".join(data_list)
