function hook_RegisterNatives() {
    let symbols = Module.enumerateSymbolsSync("libart.so");
    let addrRegisterNatives = [];

    for (let i = 0; i < symbols.length; i++) {
        let symbol = symbols[i];

        //_ZN3art3JNI15RegisterNativesEP7_JNIEnvP7_jclassPK15JNINativeMethodi
        if (symbol.name.indexOf("art") >= 0 &&
            symbol.name.indexOf("JNI") >= 0 &&
            symbol.name.indexOf("RegisterNatives") >= 0 &&
            symbol.name.indexOf("CheckJNI") < 0) {
            addrRegisterNatives.push(symbol.address);
            console.log("RegisterNatives is at =>", symbol.address, symbol.name);
        }
    }

    if (addrRegisterNatives.length > 0) {
        for (let idx in addrRegisterNatives) {
            Interceptor.attach(addrRegisterNatives[idx], {
                onEnter: function (args) {
                    // let env = args[0];
                    let java_class = args[1];
                    let class_name = Java.vm.tryGetEnv().getClassName(java_class);
                    // console.log(class_name);

                    // 只有类名为com.bilibili.nativelibrary.LibBili，才打印输出
                    const taget_class = "com.bilibili.nativelibrary.LibBili";
                    if (class_name === taget_class) {
                        console.log("\n[RegisterNatives] method_count", args[3]);
                        let methods_ptr = ptr(args[2]);
                        let methods_count = parseInt(args[3]);

                        for (let i = 0; i < methods_count; i++) {
                            // Java中函数名字
                            let name_ptr = Memory.readPointer(methods_ptr.add(i * Process.pointerSize * 3));
                            // 参数和返回值类型
                            let sig_ptr = Memory.readPointer(methods_ptr.add(i * Process.pointerSize * 3 + Process.pointerSize));
                            // C中的函数指针
                            let fn_ptr = Memory.readPointer(methods_ptr.add(i * Process.pointerSize * 3 + Process.pointerSize * 2));

                            //读取Java中函数名
                            let name = Memory.readCString(name_ptr);
                            // 参数和返回值类型
                            let sig = Memory.readCString(sig_ptr);
                            // 根据C中函数指针获取函数模块
                            let find_module = Process.findModuleByAddress(fn_ptr);

                            // 获取偏移量: fn_ptr - 模块基地址
                            let offset = ptr(fn_ptr).sub(find_module.base);
                            // console.log("[RegisterNatives] java_class:", class_name);
                            console.log("name:", name, "sig:", sig, "module_name:", find_module.name, "offset:", offset);
                            // console.log("name:", name, "module_name:", find_module.name, "offset:", offset);
                        }
                    }
                },
                // onLeave: function (retValue) {
                //     console.log("-----------------返回----------------");
                //     console.log(retValue.readUtf8String());
                // }
            });
        }
    }
}

setImmediate(hook_RegisterNatives);
// frida -U --no-pause -f tv.danmaku.bili -l 4.native.js

// RegisterNatives is at => 0xe6b73d1d _ZN3art3JNIILb0EE15RegisterNativesEP7_JNIEnvP7_jclassPK15JNINativeMethodi
// [RegisterNatives] method_count 0x8
// name: a module_name: libbili.so offset: 0x1c7d
// name: ao module_name: libbili.so offset: 0x1c83
// name: b module_name: libbili.so offset: 0x1c91
// name: s module_name: libbili.so offset: 0x1c97
// name: so module_name: libbili.so offset: 0x1c9d
// name: so module_name: libbili.so offset: 0x1cab
// name: getCpuCount module_name: libbili.so offset: 0x1cb3
// name: getCpuId module_name: libbili.so offset: 0x1cb7

// [RegisterNatives] method_count 0x8
// name: a sig: (Ljava/lang/String;)Ljava/lang/String; module_name: libbili.so offset: 0x1c7d
// name: ao sig: (Ljava/lang/String;II)Ljava/lang/String; module_name: libbili.so offset: 0x1c83
// name: b sig: (Ljava/lang/String;)Ljavax/crypto/spec/IvParameterSpec; module_name: libbili.so offset: 0x1c91
// name: s sig: (Ljava/util/SortedMap;)Lcom/bilibili/nativelibrary/SignedQuery; module_name: libbili.so offset: 0x1c97
// name: so sig: (Ljava/util/SortedMap;II)Lcom/bilibili/nativelibrary/SignedQuery; module_name: libbili.so offset: 0x1c9d
// name: so sig: (Ljava/util/SortedMap;[B)Lcom/bilibili/nativelibrary/SignedQuery; module_name: libbili.so offset: 0x1cab
// name: getCpuCount sig: ()I module_name: libbili.so offset: 0x1cb3
// name: getCpuId sig: ()I module_name: libbili.so offset: 0x1cb7
