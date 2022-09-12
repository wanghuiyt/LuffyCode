function hook_RegisterNatives() {
    Java.perform(function () {
        let Pair = Java.use("kotlin.Pair");

        Pair.$init.implementation = function (v1, v2) {
            console.log("构造方法=>", v1 + "--" + v2);
            this.$init(v1, v2);
            console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
        }

        Pair.component2.implementation = function () {
            let res = this.component2();
            console.log("device_meta=>", res);
            return res;
        }

        Pair.component1.implementation = function () {
            let res = this.component1();
            console.log("dt=>", res);
            return res;
        }
    });
}

setImmediate(hook_RegisterNatives);

// frida -U --no-pause -f tv.danmaku.bili -l 5.hook_pair.js
