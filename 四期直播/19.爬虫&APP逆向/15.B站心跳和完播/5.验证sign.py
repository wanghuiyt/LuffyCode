from hashlib import md5

data = "actual_played_time=0&aid=772508412&appkey=1d8b6e7d45233436&auto_play=0&build=6240300&c_locale=zh_CN&channel=xxl_gdt_wm_253&cid=818724896&epid=0&epid_status=&from=6&from_spmid=tm.recommend.0.0&last_play_progress_time=0&list_play_time=0&max_play_progress_time=0&mid=0&miniplayer_play_time=0&mobi_app=android&network_type=1&paused_time=0&platform=android&play_status=0&play_type=1&played_time=0&quality=64&s_locale=zh_CN&session=0148d93d4f53882bce687a408c34f56ee210329a&sid=0&spmid=main.ugc-video-detail-vertical.0.0&start_ts=0&statistics=%7B%22appId%22%3A1%2C%22platform%22%3A3%2C%22version%22%3A%226.24.0%22%2C%22abtest%22%3A%22%22%7D&sub_type=0&total_time=0&ts=1662886073&type=3&user_status=0&video_duration=23"
salt = "560c52ccd288fed045859ed18bffd973"

# &sign=4e7ac4d67bbf3addc2dbb44ea209def5
#       4e7ac4d67bbf3addc2dbb44ea209def5

obj = md5((data+salt).encode("utf-8"))
print(obj.hexdigest())
