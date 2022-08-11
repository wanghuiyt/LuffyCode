from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
# Create your views here.


def timer(request):
    now = datetime.now().strftime("%Y-%m-%d %X")
    return render(request, "app01/timer.html", {"showNow": now})


def article(request, year):
    return HttpResponse(f"{year} article")


def article_month(request, year, month):
    return HttpResponse(f"{year}年{month}月的article")


def get_login(request):
    return render(request, "login.html")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        user = request.POST.get("username")
        pwd = request.POST.get("password")
        print(user, pwd)
        if user == "123" and pwd == "123":
            # return HttpResponse("登录成功")
            return redirect("/timer/")
        else:
            return HttpResponse("用户名或者密码错误")
