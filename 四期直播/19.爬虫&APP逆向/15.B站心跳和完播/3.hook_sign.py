import sys
import frida

rdev = frida.get_remote_device()
session = rdev.attach("哔哩哔哩")

scr = """
Java.perform(function(){
    var SignedQuery = Java.use("com.bilibili.nativelibrary.SignedQuery");

    // 获取sign
    SignedQuery.toString.implementation = function(){
        var res = this.toString();
        console.log("sign=>",res);
        console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Throwable").$new()));
        return res;
    }
    
    var libbili = Module.findBaseAddress("libbili.so");
    var s_func = libbili.add(0x22b0 + 1);
    
    Interceptor.attach(s_func, {
        onEnter: function(args){
            // args[0] 
            // args[1] 明文字符串
            // args[2] 明文字符串长度
            console.log("执行update,长度是=>",args[2]);
            console.log(hexdump(args[1], {length: args[2].toInt32()})); 
        },
        onLeave: function(args){
            console.log("=======================结束=======================");     
        }
    });

});
"""

script = session.create_script(scr)

script.load()
sys.stdin.read()

# 执行update,长度是=> 0x2c6
#            0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF
# ccef6e00  61 63 74 75 61 6c 5f 70 6c 61 79 65 64 5f 74 69  actual_played_ti
# ccef6e10  6d 65 3d 30 26 61 69 64 3d 37 37 32 35 30 38 34  me=0&aid=7725084
# ccef6e20  31 32 26 61 70 70 6b 65 79 3d 31 64 38 62 36 65  12&appkey=1d8b6e
# ccef6e30  37 64 34 35 32 33 33 34 33 36 26 61 75 74 6f 5f  7d45233436&auto_
# ccef6e40  70 6c 61 79 3d 30 26 62 75 69 6c 64 3d 36 32 34  play=0&build=624
# ccef6e50  30 33 30 30 26 63 5f 6c 6f 63 61 6c 65 3d 7a 68  0300&c_locale=zh
# ccef6e60  5f 43 4e 26 63 68 61 6e 6e 65 6c 3d 78 78 6c 5f  _CN&channel=xxl_
# ccef6e70  67 64 74 5f 77 6d 5f 32 35 33 26 63 69 64 3d 38  gdt_wm_253&cid=8
# ccef6e80  31 38 37 32 34 38 39 36 26 65 70 69 64 3d 30 26  18724896&epid=0&
# ccef6e90  65 70 69 64 5f 73 74 61 74 75 73 3d 26 66 72 6f  epid_status=&fro
# ccef6ea0  6d 3d 36 26 66 72 6f 6d 5f 73 70 6d 69 64 3d 74  m=6&from_spmid=t
# ccef6eb0  6d 2e 72 65 63 6f 6d 6d 65 6e 64 2e 30 2e 30 26  m.recommend.0.0&
# ccef6ec0  6c 61 73 74 5f 70 6c 61 79 5f 70 72 6f 67 72 65  last_play_progre
# ccef6ed0  73 73 5f 74 69 6d 65 3d 30 26 6c 69 73 74 5f 70  ss_time=0&list_p
# ccef6ee0  6c 61 79 5f 74 69 6d 65 3d 30 26 6d 61 78 5f 70  lay_time=0&max_p
# ccef6ef0  6c 61 79 5f 70 72 6f 67 72 65 73 73 5f 74 69 6d  lay_progress_tim
# ccef6f00  65 3d 30 26 6d 69 64 3d 30 26 6d 69 6e 69 70 6c  e=0&mid=0&minipl
# ccef6f10  61 79 65 72 5f 70 6c 61 79 5f 74 69 6d 65 3d 30  ayer_play_time=0
# ccef6f20  26 6d 6f 62 69 5f 61 70 70 3d 61 6e 64 72 6f 69  &mobi_app=androi
# ccef6f30  64 26 6e 65 74 77 6f 72 6b 5f 74 79 70 65 3d 31  d&network_type=1
# ccef6f40  26 70 61 75 73 65 64 5f 74 69 6d 65 3d 30 26 70  &paused_time=0&p
# ccef6f50  6c 61 74 66 6f 72 6d 3d 61 6e 64 72 6f 69 64 26  latform=android&
# ccef6f60  70 6c 61 79 5f 73 74 61 74 75 73 3d 30 26 70 6c  play_status=0&pl
# ccef6f70  61 79 5f 74 79 70 65 3d 31 26 70 6c 61 79 65 64  ay_type=1&played
# ccef6f80  5f 74 69 6d 65 3d 30 26 71 75 61 6c 69 74 79 3d  _time=0&quality=
# ccef6f90  36 34 26 73 5f 6c 6f 63 61 6c 65 3d 7a 68 5f 43  64&s_locale=zh_C
# ccef6fa0  4e 26 73 65 73 73 69 6f 6e 3d 30 31 34 38 64 39  N&session=0148d9
# ccef6fb0  33 64 34 66 35 33 38 38 32 62 63 65 36 38 37 61  3d4f53882bce687a
# ccef6fc0  34 30 38 63 33 34 66 35 36 65 65 32 31 30 33 32  408c34f56ee21032
# ccef6fd0  39 61 26 73 69 64 3d 30 26 73 70 6d 69 64 3d 6d  9a&sid=0&spmid=m
# ccef6fe0  61 69 6e 2e 75 67 63 2d 76 69 64 65 6f 2d 64 65  ain.ugc-video-de
# ccef6ff0  74 61 69 6c 2d 76 65 72 74 69 63 61 6c 2e 30 2e  tail-vertical.0.
# ccef7000  30 26 73 74 61 72 74 5f 74 73 3d 30 26 73 74 61  0&start_ts=0&sta
# ccef7010  74 69 73 74 69 63 73 3d 25 37 42 25 32 32 61 70  tistics=%7B%22ap
# ccef7020  70 49 64 25 32 32 25 33 41 31 25 32 43 25 32 32  pId%22%3A1%2C%22
# ccef7030  70 6c 61 74 66 6f 72 6d 25 32 32 25 33 41 33 25  platform%22%3A3%
# ccef7040  32 43 25 32 32 76 65 72 73 69 6f 6e 25 32 32 25  2C%22version%22%
# ccef7050  33 41 25 32 32 36 2e 32 34 2e 30 25 32 32 25 32  3A%226.24.0%22%2
# ccef7060  43 25 32 32 61 62 74 65 73 74 25 32 32 25 33 41  C%22abtest%22%3A
# ccef7070  25 32 32 25 32 32 25 37 44 26 73 75 62 5f 74 79  %22%22%7D&sub_ty
# ccef7080  70 65 3d 30 26 74 6f 74 61 6c 5f 74 69 6d 65 3d  pe=0&total_time=
# ccef7090  30 26 74 73 3d 31 36 36 32 38 38 36 30 37 33 26  0&ts=1662886073&
# ccef70a0  74 79 70 65 3d 33 26 75 73 65 72 5f 73 74 61 74  type=3&user_stat
# ccef70b0  75 73 3d 30 26 76 69 64 65 6f 5f 64 75 72 61 74  us=0&video_durat
# ccef70c0  69 6f 6e 3d 32 33                                ion=23
# =======================结束=======================
# 执行update,长度是=> 0x8
#            0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF
# aeb76cc0  35 36 30 63 35 32 63 63                          560c52cc
# =======================结束=======================
# 执行update,长度是=> 0x8
#            0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF
# aeb76cc0  64 32 38 38 66 65 64 30                          d288fed0
# =======================结束=======================
# 执行update,长度是=> 0x8
#            0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF
# aeb76cc0  34 35 38 35 39 65 64 31                          45859ed1
# =======================结束=======================
# 执行update,长度是=> 0x8
#            0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF
# aeb76cc0  38 62 66 66 64 39 37 33                          8bffd973
# =======================结束=======================
# 执行update,长度是=> 0x12
#            0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF
# aff2f064  80 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
# aff2f074  00 00                                            ..
# =======================结束=======================
# 执行update,长度是=> 0x8
#            0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF
# aeb76c04  30 17 00 00 00 00 00 00                          0.......
# =======================结束=======================

# sign=> actual_played_time=0&aid=772508412&appkey=1d8b6e7d45233436&auto_play=0&build=6240300&c_locale=zh_CN&channel=xxl_gdt_wm_253&cid=818724896&epid=0&epid_status=&from=6&from_spmid=tm.recommend.0.0&last_play_progress_time=0&list_play_time=0&max_play_progress_time=0&mid=0&miniplayer_play_time=0&mobi_app=android&network_type=1&paused_time=0&platform=android&play_status=0&play_type=1&played_time=0&quality=64&s_locale=zh_CN&session=0148d93d4f53882bce687a408c34f56ee210329a&sid=0&spmid=main.ugc-video-detail-vertical.0.0&start_ts=0&statistics=%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%226.24.0%22%2C%22abtest%22%3A%22%22%7D&sub_type=0&total_time=0&ts=1662886073&type=3&user_status=0&video_duration=23&sign=4e7ac4d67bbf3addc2dbb44ea209def5
# java.lang.Throwable
# 	at com.bilibili.nativelibrary.SignedQuery.toString(Native Method)
# 	at com.bilibili.okretro.f.a.c(BL:16)
# 	at com.bilibili.okretro.f.a.a(BL:6)
# 	at com.bilibili.okretro.d.a.execute(BL:24)
# 	at com.bilibili.okretro.d.a$a.run(BL:2)
# 	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1167)
# 	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:641)
# 	at java.lang.Thread.run(Thread.java:920)


# salt: 560c52ccd288fed045859ed18bffd973
