import uuid
from hashlib import md5
from flask import Flask, request, jsonify

app = Flask(__name__)


def myMd5(data):
    obj = md5()
    obj.update(data.encode("utf-8"))
    return obj.hexdigest()


@app.route("/auth", methods=["POST"])
def auth():
    print(request)
    # 1.获取各个数据
    # user = request.form.get("user")
    # pwd = request.form.get("pwd")
    # sign = request.form.get("sign")
    # 2.sign签名的校验
    # if sign != myMd5(f"password{pwd}username{user}"):
    #     return "失败"
    # 3.根据用户名和密码去数据库校验

    return jsonify({"status": True, "token": str(uuid.uuid4())})


if __name__ == '__main__':
    # app.run(host="192.168.0.121", ssl_context="adhoc")
    # f78a7f44
    app.run(host="192.168.0.121", port=5000)
