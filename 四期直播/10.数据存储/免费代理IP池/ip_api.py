"""
负责给用户提供可用IP
1.提供api接口的模块 sanic sanic_cors
给外界提供一个http接口，外界通过访问http://xxxx/get_proxy
"""
from sanic import Sanic, json
from sanic_cors import CORS
from proxy_redis import ProxyRedis

r = ProxyRedis()

# 1.创建app
app = Sanic("ip")  # 随便给个名字
# 2.解决跨域
CORS(app)

# 3.能够处理http请求的函数
@app.route("/get_proxy")
def getProxy(req):
    ip = r.get_enable_proxy()
    print(ip)
    return json({"ip": ip})


def run():
    app.run(host="127.0.0.1", port=5804)


if __name__ == '__main__':
    run()



