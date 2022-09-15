import hmac
from hashlib import sha1


data_string = "13552app_build=1031&app_version=5.32.1&bt_ck=1&bundle_id=com.zhihu.android&cp_ct=8&cp_fq=2000000&cp_tp=0&cp_us=100.0&d_n=Android%20Bluedroid&fr_mem=461&fr_st=211570&latitude=0.0&longitude=0.0&mc_ad=7E%3A62%3A5D%3A66%3A7E%3A62&mcc=cn&nt_st=1&ph_br=Redmi&ph_md=21091116AC&ph_os=Android%2012&ph_sn=unknown&pvd_nm=%E5%B0%8F%E7%B1%B3%E7%A7%BB%E5%8A%A8&tt_mem=512&tt_st=231693&tz_of=288001663250501"
salt = "dd49a835-56e7-4a0f-95b5-efd51ea5397f"

obj = hmac.new(salt.encode("utf-8"), data_string.encode("utf-8"), sha1)
print(obj.hexdigest())

# b22fcc3caa15d71118e9852578e4fdedde23e27b
# b22fcc3caa15d71118e9852578e4fdedde23e27b
