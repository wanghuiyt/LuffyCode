from django.shortcuts import render, HttpResponse
from django.core.handlers.wsgi import WSGIRequest
# Create your views here.


def index(request: WSGIRequest):
    print(request.method)
    print(request.path)  # /
    print(request.get_full_path())  # /?a=1
    print(request.META.get("REMOTE_ADDR"))  # IP
    # 请求数据
    print(request.GET)
    print(request.POST)
    return HttpResponse("OK")
