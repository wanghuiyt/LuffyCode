from django.shortcuts import render, HttpResponse
from datetime import datetime
# Create your views here.


def timer(request):
    now = datetime.now().strftime("%Y-%m-%d %X")
    return render(request, "app01/timer.html", {"showNow": now})


def article(request, year):
    return HttpResponse(f"{year} article")


def article_month(request, year, month):
    return HttpResponse(f"{year}年{month}月的article")

