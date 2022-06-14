import requests

url = "https://desk-fd.zol-img.com.cn/t_s208x130c5/g7/M00/02/0A/ChMkLGKhVHyIa9vaAAJ7oS7tvVoAAEKawKjEWwAAnu5823.jpg"

resp = requests.get(url)
# print(resp.text)  # 访问的url并不是文本
# print(resp.content)
content = resp.content
with open("haha.jgp", mode="wb") as f:
    f.write(content)

