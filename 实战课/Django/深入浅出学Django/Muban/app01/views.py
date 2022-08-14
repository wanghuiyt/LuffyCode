import datetime

from django.shortcuts import render

# Create your views here.
class Stu(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age


def index(request):
    name = "yuan"
    books  = ["西游记", "三国演义", "金瓶梅", "红楼梦"]
    info = {"name": "yuan", "age":18}
    stu = Stu("xiaoming", 23)
    now = datetime.datetime.now()
    age = 10
    filesize = 203456984
    link = '<a href="http://www.baidu.com">click</a>'
    # return render(request, "index.html", {"name": name, "books": lst, "info": info})
    return render(request, "index.html", locals())

