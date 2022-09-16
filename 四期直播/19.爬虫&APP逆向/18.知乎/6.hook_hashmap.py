import sys

import frida

rdev = frida.get_remote_device()
session = rdev.attach("知乎")

scr = """
Java.perform(function(){
    let HashMap = Java.use("java.util.HashMap");
    
    HashMap.put.implementation = function(key,value){
        if(key==="x-zse-96"){
            console.log(key, value);
            console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
        }
        
        let res = this.put(key,value);
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

