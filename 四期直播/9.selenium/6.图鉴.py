import base64
import json
import requests


def base64_api(uname, pwd, img, typeid):
    with open(img, "rb") as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result["success"]:
        return result["data"]["result"]
    else:
        return result["message"]


if __name__ == '__main__':
    img_path = "C:/Users/Administrator/Desktop/file.jpg"
    result = base64_api(uname="q6035945", pwd="q6035945", img=img_path, typeid=3)
    print(result)


