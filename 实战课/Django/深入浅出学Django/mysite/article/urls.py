from django.urls import re_path
from article import views

urlpatterns = [
    # 正则匹配
    re_path('(\d{4})$', views.article),  # 一定要分组
    # re_path('^article/(\d{4})/(\d{1,2})$', v1.article_month)
    # 有名分组
    re_path('(?P<year>\d{4})/(?P<month>\d{1,2})$', views.article_month)
]
