"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from app01 import views as v1
from app02 import views as v2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('timer/', v1.timer),
    path('', v2.index),
    # 正则匹配
    # re_path('^article/(\d{4})$', v1.article),  # 一定要分组
    # re_path('^article/(\d{4})/(\d{1,2})$', v1.article_month)
    # 有名分组
    # re_path('^article/(?P<year>\d{4})/(?P<month>\d{1,2})$', v1.article_month)
    # 路由分发
    re_path("^article/", include("article.urls"))
]
