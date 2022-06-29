import requests

# https://www.pearvideo.com/videoStatus.jsp?contId=1765893&mrd=0.8947503356509281
main_url = "https://www.pearvideo.com/video_1765893"  # input("请输入你需要的爬取的梨视频的地址:")
contId = main_url.split("_")[-1]
url = f"https://www.pearvideo.com/videoStatus.jsp?contId={contId}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "Cookie": "__secdyid=cdb5fa3ab39185bdbf079cef50865ea28be3c79a665d9057021656138298; acw_tc=2f61f27616561382984367731e20fe906c9dd99a9e73a54b37a316dea661ea; JSESSIONID=FBE8B5538A5D6CAD5226D2D06E8A543D; PEAR_UUID=7159ff6f-33fb-456f-8e9a-fb7e6a3d57f8; _uab_collina=165613829853941600265944; Hm_lvt_9707bc8d5f6bba210e7218b8496f076a=1656138299; p_h5_u=07240649-3459-4D7F-AA22-F3241CC8F1FD; Hm_lpvt_9707bc8d5f6bba210e7218b8496f076a=1656138310; SERVERID=ed8d5ad7d9b044d0dd5993c7c771ef48|1656138331|1656138298",
    "Referer": main_url  # 处理防盗链
}

resp = requests.get(url, headers=headers)
# print(resp.json())
dic = resp.json()
srcUrl = dic["videoInfo"]["videos"]["srcUrl"]
systemTime = dic["systemTime"]
srcUrl = srcUrl.replace(systemTime, f"cont-{contId}")
# print(srcUrl)
resp = requests.get(srcUrl, headers=headers)
# fileName = srcUrl.split("/")[-1].replace("-", "")
fileName = f"{contId}.mp4"
with open(fileName, mode="wb") as f:
    f.write(resp.content)
print("下载完成")

