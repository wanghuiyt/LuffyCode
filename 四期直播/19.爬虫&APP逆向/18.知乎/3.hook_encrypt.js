function hook_RegisterNatives() {
    Java.perform(function(){
        let CloudIDHelper = Java.use("com.zhihu.android.cloudid.CloudIDHelper");

        CloudIDHelper.encrypt.implementation = function(str, str2, str3, str4, str5, str6, str7) {
            console.log("str=>", str);
            console.log("str2=>", str2);
            console.log("str3=>", str3);
            console.log("str4=>", str4);
            console.log("str5=>", str5);
            console.log("str6=>", str6);
            console.log("str7=>", str7);
            let res = this.encrypt(str, str2, str3, str4, str5, str6, str7);
            console.log("res=>", res);
            return res;
        }
    });
}

setImmediate(hook_RegisterNatives);

// frida -U --no-pause -f com.zhihu.android -l 3.hook_encrypt.js

// str=> 2
// str2=> null
// str3=> null
// str4=> app_build=1031&app_version=5.32.1&bt_ck=1&bundle_id=com.zhihu.android&cp_ct=8&cp_fq=2000000&cp_tp=0&cp_us=100.0&d_n=Android%20Bluedroid&fr_mem=461&fr_st=211570&latitude=0.0&longitude=0.0&mc_ad=7E%3A62%3A5D%3A66%3A7E%3A62&mcc=cn&nt_st=1&ph_br=Redmi&ph_md=21091116AC&ph_os=Android%2012&ph_sn=unknown&pvd_nm=%E5%B0%8F%E7%B1%B3%E7%A7%BB%E5%8A%A8&tt_mem=512&tt_st=231693&tz_of=28800
// str5=> 1355
// str6=> 1663250501
// str7=> dd49a835-56e7-4a0f-95b5-efd51ea5397f
// res=> b22fcc3caa15d71118e9852578e4fdedde23e27b

