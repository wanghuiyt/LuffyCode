import json

data = "callback=jsonp1&guid=l7d1stvh_ql78atkhbfq&platform=4330701&vid=i000075mu8r&defn=auto&charge=0&defaultfmt=auto&otype=json&defnpayver=1&appVer=1.2.10&sphttps=1&sphls=1&spwm=4&dtype=3&defsrc=1&encryptVer=8.1&sdtfrom=4330701&cKey=--0122F46409D16419761E7CF64C400CF7C7C22BE9AA1EEDA5B516691325920A823DB2AFC68FE3D18F3F1F9517D4CE7C46AC7902D56BCC4BF41CAF62561A7EAD648E7516AB3B7645793F13EC8BC7E85728DB8EB808A667E6774AD4826543D30CC36A51DB29D3689630566A66422FB12382A67EA8B143D916EB0F1065F3A381F4F0F04DA0380025C9475E1FD4F563A5EDB380C7F124B384EFA827A982D1C7B647F172&panoramic=false&flowid=l7d1tzgd_g0khd335w2"

data = "aweme_id=7141673857936559392&cursor=0&count=20&address_book_access=2&gps_access=2&forward_page_type=1&channel_id=0&city=310000&hotsoon_filtered_count=0&hotsoon_has_more=0&follower_count=0&is_familiar=0&page_source=0&manifest_version_code=110501&_rticket=1663387949717&app_type=normal&iid=3373723980667831&channel=gdt_growth14_big_yybwz&device_type=21091116AC&language=zh&cpu_support64=true&host_abi=armeabi-v7a&resolution=1080*2260&openudid=bd8ffbbebe2663f4&update_version_code=11509900&cdid=6750e48d-ceec-4674-b5c2-7faa571555b8&os_api=31&mac_address=7E%3A62%3A5D%3A66%3A7E%3A62&dpi=440&oaid=705a52036f49ecc7&ac=wifi&device_id=3831116258620196&mcc_mnc=46001&os_version=12&version_code=110500&app_name=aweme&version_name=11.5.0&device_brand=Redmi&ssmix=a&device_platform=android&aid=1128&ts=1663387948"

data_dict = {item.split("=")[0]: item.split("=")[1] for item in data.split("&")}
print(json.dumps(data_dict, indent=2))

