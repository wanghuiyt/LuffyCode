import gzip
from hashlib import md5

body = '{"magic_tag":"ss_app_log","header":{"display_name":"抖音短视频","update_version_code":11509900,"manifest_version_code":110501,"app_version_minor":"","aid":1128,"channel":"gdt_growth14_big_yybwz","appkey":"57bfa27c67e58e7d920028d3","package":"com.ss.android.ugc.aweme","app_version":"11.5.0","version_code":110500,"sdk_version":"2.14.0-alpha.4","sdk_target_version":29,"git_hash":"c1aa4085","os":"Android","os_version":"12","os_api":31,"device_model":"21091116AC","device_brand":"Redmi","device_manufacturer":"Xiaomi","cpu_abi":"armeabi-v7a","release_build":"b44f245_20200615_436d6cbc-aecc-11ea-bfa1-02420a000026","density_dpi":440,"display_density":"mdpi","resolution":"2260x1080","language":"zh","mc":"7E:62:5D:66:7E:62","timezone":8,"access":"wifi","not_request_sender":0,"carrier":"小米移动","mcc_mnc":"46001","rom":"MIUI-V13.0.6.0.SGBCNXM","rom_version":"miui_V130_V13.0.6.0.SGBCNXM","cdid":"dc60be44-e080-4f6f-a67a-4b25507cc602","sig_hash":"aea615ab910015038f73c47e45d21466","openudid":"bd8ffbbebe2663f4","clientudid":"1e007b00-2d09-48bf-b724-20a8d59f39a5","sim_serial_number":[],"region":"CN","tz_name":"Asia\/Shanghai","tz_offset":28800,"sim_region":"cn","oaid":{"req_id":"b97c560e-d43f-4253-90f0-e7ca9d999af4","hw_id_version_code":"null","take_ms":"20","is_track_limited":"null","query_times":"1","id":"705a52036f49ecc7","time":"1663466045007"},"oaid_may_support":true,"req_id":"73c0f087-2262-47ef-a69d-723cb186c5e3","custom":{"filter_warn":0,"web_ua":"Mozilla\/5.0 (Linux; Android 12; 21091116AC Build\/SP1A.210812.016; wv) AppleWebKit\/537.36 (KHTML, like Gecko) Version\/4.0 Chrome\/99.0.4844.88 Mobile Safari\/537.36"},"pre_installed_channel":"ame_xiaomi2020_1311_yz1","apk_first_install_time":1663464114426,"is_system_app":0,"sdk_flavor":"china"},"_gen_time":1663466056580}'

gzip_body = gzip.compress(body.encode("utf-8"))
java_gzip_body = bytearray(gzip_body)
java_gzip_body[3:10] = [0, 0, 0, 0, 0, 0, 0]

obj = md5()
obj.update(bytes(java_gzip_body))
x_ss_stud = obj.hexdigest().upper()
print(x_ss_stud)

# CA9848B429A06BB8753544F69E3F2CCB
# CA9848B429A06BB8753544F69E3F2CCB
