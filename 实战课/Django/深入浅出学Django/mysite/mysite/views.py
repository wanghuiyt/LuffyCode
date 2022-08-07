from django.shortcuts import HttpResponse
from datetime import datetime


def timer(request):
    now = datetime.now().strftime("%Y-%m-%d %X")
    return HttpResponse(now)
