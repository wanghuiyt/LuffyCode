import json

from flask import Flask, render_template, request, make_response

app = Flask("javascript")


@app.route("/")
def jay():
    print("我是一个普通函数")
    # f = open("templates/index.html", mode="r", encoding="utf-8")
    # c = f.read()
    return render_template("index1.html", name="alex", age=18)


@app.route("/hehe", methods=["POST"])
def su():
    # GET
    # print("1245")
    # p = request.args.get("page")
    # print(p)
    # print(request.headers)
    # s = make_response(p)
    # s.set_cookie("a", "b")

    # POST
    data = request.form.get("xxm")  # Form data
    print(data)
    # return json.dumps({"name": "alex", "age": 18})
    # 服务器端可不可以返回一段js代码
    cb = request.args.get("callback")
    data = json.dumps({"name": "alex", "age": 18})
    s = make_response(f"{cb}({data})")
    s.set_cookie("a", "b")
    return s


@app.route("/haha", methods=["POST"])
def haha():
    print("我是hahaha")
    name = request.json.get("name")
    age = request.json.get("age")
    return json.dumps({"name": name, "age": age})


if __name__ == '__main__':
    app.run(debug=True)
