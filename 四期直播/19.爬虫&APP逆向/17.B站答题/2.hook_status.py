import sys
import frida

rdev = frida.get_remote_device()
session = rdev.attach("哔哩哔哩")

scr = """
Java.perform(function(){
    var ChameleonAnswerView = Java.use("tv.danmaku.bili.ui.main2.mine.widgets.ChameleonAnswerView");
    
    ChameleonAnswerView.e.overload('java.lang.String', 'java.lang.String', 'java.lang.String').implementation = function(str,str2,str3){
        console.log("str=>", str);
        console.log("str2=>", str2);
        console.log("str3=>", str3);
        
        this.e(str,str2,str3);
    }
    
});
"""

script = session.create_script(scr)


def on_message(message, data):
    print(message, data)


script.on("message", on_message)
script.load()
sys.stdin.read()
