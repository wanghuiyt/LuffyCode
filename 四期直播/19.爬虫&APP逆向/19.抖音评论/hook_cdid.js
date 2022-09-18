function hook_RegisterNatives(){
    Java.perform(function(){
        var cls = Java.use("com.ss.android.deviceregister.d.a$1");

        cls.a.implementation = function(arg4){
            var res = this.a(arg4);
            console.log("res=>",res);
            console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
            return res;
        }

        // hook this.k
        var c = Java.use("com.ss.android.deviceregister.b.c");

        c.c.implementation = function(){
            // console.log(this.k);  // 默认是去找k函数
            send(this.k.value)
            // send(字节数组)  将值交给python进行处理
            // console.log(字节数组)=>object  console.log(JSON.stringify(字节数组))=>字符串
            return this.c();
        }

        // hook 请求头参数和返回值
        var tt = Java.use("com.ss.sys.ces.gg.tt$1");

        tt.a.implementation = function(str, map){
            console.log("参数1=>", str);

            var Map = Java.use("java.util.HashMap");
            var obj1 = Java.cast(map, Map);
            console.log("参数2=>", obj1.toString());

            var res = this.a(str, map);
            var obj2 = Java.cast(res, Map);
            console.log("返回值=>", obj2.toString());
            return res;
        }
    });
}
setImmediate(hook_RegisterNatives);

// frida -U --no-pause -f com.ss.android.ugc.aweme -l hook_cdid.js

//       6750e48d-ceec-4674-b5c2-7faa571555b8
// res=> 6750e48d-ceec-4674-b5c2-7faa571555b8
// java.lang.Throwable
//         at com.ss.android.deviceregister.d.a$1.a(Native Method)
//         at com.ss.android.deviceregister.d.h.b(SourceFile:16973833)
//         at com.ss.android.deviceregister.d.a.a(SourceFile:16908296)
//         at com.ss.android.common.applog.NetUtil.putCommonParams(SourceFile:34079342)
//         at com.ss.android.ugc.aweme.legoImp.task.CrashSdkInitTask$a.a(SourceFile:262176)
//         at com.bytedance.crash.runtime.c.b(SourceFile:393225)
//         at com.bytedance.crash.upload.e.run(SourceFile:393410)
//         at android.os.Handler.handleCallback(Handler.java:938)
//         at android.os.Handler.dispatchMessage(Handler.java:99)
//         at android.os.Looper.loopOnce(Looper.java:210)
//         at android.os.Looper.loop(Looper.java:299)
//         at com.bytedance.crash.runtime.q$c.onLooperPrepared(SourceFile:327712)
//         at android.os.HandlerThread.run(HandlerThread.java:66)

// message: {'type': 'send', 'payload': '<instance: com.ss.android.deviceregister.b.a.a, $className: com.ss.android.deviceregister.c>'} data: None

// 参数1=> https://api5-normal-c-lq.amemv.com/aweme/v2/comment/list/?aweme_id=7144263631901871401&cursor=0&count=20&address_book_access=2&gps_access=2&forward_page_type=1&channel_id=0&city=310000&hotsoon_filtered_count=0&hotsoon_has_more=0
// &follower_count=0&is_familiar=0&page_source=0&manifest_version_code=110501&_rticket=1663416591270&app_type=normal&iid=3373723980667831&channel=gdt_growth14_big_yybwz&device_type=21091116AC&language=zh&cpu_support64=true&host_abi=armeabi
// -v7a&resolution=1080*2260&openudid=bd8ffbbebe2663f4&update_version_code=11509900&cdid=a5ee1207-587c-4050-82dc-1337b4feaef3&os_api=31&mac_address=7E%3A62%3A5D%3A66%3A7E%3A62&dpi=440&oaid=705a52036f49ecc7&ac=wifi&device_id=383111625862019
// 6&mcc_mnc=46001&os_version=12&version_code=110500&app_name=aweme&version_name=11.5.0&device_brand=Redmi&ssmix=a&device_platform=android&aid=1128&ts=1663416590
// 参数2=> {
// x-tt-trace-id=[00-4b5ae52c0dd9c6143b033244dcb60468-4b5ae52c0dd9c614-01],
// cookie=[install_id=3373723980667831; ttreq=1$401906cb23f7036f05edbe1596f991af9cb5c048; odin_tt=545131b8f279cea639a7b40906dbe78980d69d8571117abfb33b742d665
// 2c9b2bab42e3bc296dc14790b9a6939ca0ad906d2e2babc36b02529ddef361d97aaa6490ca48d21d4627d143ca35f39478c90],
// sdk-version=[1], x-ss-dp=[1128], accept-encoding=[gzip, deflate, br], x-ss-req-ticket=[1663416591268],
// user-agent=[com.ss.android.ugc.aweme/110501 (Linux; U; Android 12; zh_CN; 21091116AC; Build/SP1A.210812.016; Cronet/TTNetVersion:3c28619c 2020-05-19 QuicVersion:0144d358 2020-03-24)]
// }
// 返回值=> {X-Khronos=1663416591, X-Gorgon=040468ef0000b6d63bc8acb5aea4f957349afc2382376f0d8352}
