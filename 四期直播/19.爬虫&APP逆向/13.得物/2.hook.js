function hook_RegisterNatives(){
    Java.perform(function(){
        var Builder = Java.use("okhttp3.OkHttpClient$Builder");
        Builder.proxy.implementation = function(proxy){
            return this.proxy(null);
        }
    })
}
setImmediate(hook_RegisterNatives);

// frida -U --no-pause -f com.shizhuang.duapp -l 2.hook.js
