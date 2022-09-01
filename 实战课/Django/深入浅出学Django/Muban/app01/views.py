import datetime
from app01.models import Student
from django.shortcuts import render, HttpResponse


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


def add_stu(request):
    # 方式一
    # stu = Student(name="yuan", age=23, birth_day="1998-12-12")
    # stu.save()
    # print(stu.id)

    # 方式二
    s2 = Student.objects.create(name="rain", age=24, birth_day="1997-12-12")
    print(s2.name)
    print(s2.id)

    return HttpResponse("添加成功")


def select_stu(request):
    # all() 返回值是QuerySet对象
    # student_list = Student.objects.all()
    # # print(student_list)
    # for stu in student_list:
    #     print(stu.name, stu.age, stu.birth_day)

    # filter() 返回query对象
    # q2 = Student.objects.filter(age=24)
    # print(q2)

    # get() 返回一个对象（有且只有一条记录，没有或者多条都会报错）
    # s = Student.objects.get(age=23)
    # print(s.age)

    # exclude() 排除符合条件的结果，返回值是QuerySet对象
    # Student.objects.exclude(age=23)

    # first()  last() 返回一个模型类对象
    # Student.objects.all().first()
    # Student.objects.all().last()

    # order_by 排序 前面加-表示倒序
    # reverse() 反转
    # q3 = Student.objects.all().order_by("-age", "-id")
    # print(q3)

    # count() 返回查询对象的个数
    # n = Student.objects.all().count()
    # print(n)

    # 只要前面返回QuerySet对象，就可以链式操作
    Student.objects.all().filter(age=23).order_by("-id").count()

    return HttpResponse("查询成功")




































