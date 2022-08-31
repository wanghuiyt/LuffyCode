import datetime
from django.shortcuts import render


# Create your views here.
class Stu(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age


def index(request):
    name = "yuan"
    books = ["西游记", "三国演义", "金瓶梅", "红楼梦"]
    info = {"name": "yuan", "age": 18}
    stu = Stu("xiaoming", 23)
    now = datetime.datetime.now()
    age = 10
    filesize = 203456984
    link = '<a href="http://www.baidu.com">click</a>'
    user = "yuan"
    score = 98
    book_list = [
        {"id": 11, "name": "Python基础入门", "price": 130.00},
        {"id": 17, "name": "GO基础入门", "price": 230.00},
        {"id": 23, "name": "PHP基础入门", "price": 330.00},
        {"id": 44, "name": "Java基础入门", "price": 730.00},
        {"id": 51, "name": "C++基础入门", "price": 300.00},
        {"id": 56, "name": "C#基础入门", "price": 100.00},
        {"id": 57, "name": "前端基础入门", "price": 380.00},
    ]
    # return render(request, "index.html", {"name": name, "books": lst, "info": info})
    return render(request, "index.html", locals())


def order(request):
    return render(request, "order.html")



