from hashlib import sha256

data = "aid=382382737&auto_play=0&build=6240300&cid=555494369&did=Lhp8SitJf0dwR3ZAc0JySws5CDgBMAEwBkcE&epid=&from_spmid=tm.recommend.0.0&ftime=1662674999&lv=0&mid=0&mobi_app=android&part=0&sid=0&spmid=main.ugc-video-detail-vertical.0.0&stime=1662678801&sub_type=0&type=3"

salt = "9cafa6466a028bfb"
obj = sha256()
obj.update(data.encode("utf-8"))
obj.update(salt.encode("utf-8"))
res = obj.hexdigest()
print(res)
#              2ea8e955a7ef7534c83340deb99eb51d3afbe578daa1059be4ebe581832e65a9
# sha256加密后= 2ea8e955a7ef7534c83340deb99eb51d3afbe578daa1059be4ebe581832e65a9
