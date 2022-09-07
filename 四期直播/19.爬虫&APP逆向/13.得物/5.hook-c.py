import sys
import frida

rdev = frida.get_remote_device()
session = rdev.attach("得物(毒)")

scr = """
Java.perform(function () {

    // hook-c
    // var str_name_so = "libJNIEncrypt.so"  // 需要hook的so名称
    // var n_addr_func_offset = 0x00001F5C;  // 需要hook的函数的偏移量
    // var n_addr_so = Module.findBaseAddress(str_name_so)  // 加载到内存后 函数地址 = so地址 + 函数偏移
    // var n_addr_func = parseInt(n_addr_so) + n_addr_func_offset;
    // var addr_func = new NativePointer(n_addr_func);
    
    var addr_func = Module.findExportByName("libJNIEncrypt.so", "AES_128_ECB_PKCS5Padding_Encrypt");
    
    Interceptor.attach(addr_func, {
        onEnter: function(args){
            console.log("----------------执行函数---------------");

            console.log("-----------------参数1----------------");
            console.log(args[0].readUtf8String());

            console.log("-----------------参数2----------------");
            console.log(args[1].readUtf8String());
        },
        onLeave: function(retValue){
            console.log("-----------------返回----------------");
            console.log(retValue.readUtf8String());
        }
    })
});
"""

script = session.create_script(scr)
script.load()
sys.stdin.read()
