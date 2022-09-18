import sys
import frida

rdev = frida.get_remote_device()
session = rdev.attach("抖音短视频")

scr = """
Java.perform(function(){
    var AwemeStatisticsStructV2 = Java.use("com.ss.ugc.aweme.proto.AwemeStatisticsStructV2");
    
    AwemeStatisticsStructV2.$init.overload('java.lang.String', 'java.lang.Long', 
        'java.lang.Long', 'java.lang.Long', 'java.lang.Long', 'java.lang.Long', 'java.lang.Long', 'java.lang.Integer', 'java.lang.Integer', 'java.lang.Long', 'okio.ByteString').implementation = function(str,l,l2,l3,l4,l5,l6,num,num2,l7,byteString){
        console.log("str=>", str);
        this.$init(str, l, l2, l3, l4, l5, l6, num, num2, l7, byteString);
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
        // return res;
    };
});
"""

script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)
script.load()
sys.stdin.read()
