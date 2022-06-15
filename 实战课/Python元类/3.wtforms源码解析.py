from flask import Flask
from wtforms import Form
from wtforms.fields import  simple

app = Flask(__name__, template_folder="templates")
app.debug = True


class FormMeta(type):
    def __init__(cls, name, bases, attrs):
        type.__init__(cls, name, bases, attrs)
        cls._unbound_fields = None
        cls._wtforms_meta = None

    def __call__(cls, *args, **kwargs):
        pass


def with_metaclass(meta, base=object):
    # FormMeta("NewBase", (BaseForm,), {})
    #     type("NewBase", (BaseForm,), {})
    return meta("NewBase", (base,), {})


"""
class NewBase(BaseForm, metaclass=FormMeta):
    pass

class Form(NewBase):
"""


class Form(with_metaclass(FormMeta, BaseForm)):
    pass


# LoginForm其实是由 FormMeta 创建的
# 1.创建类时，会执行FormMeta 的__new__和__init__，内部在类中添加了两个类变量 _unbound_fields 和 _wtforms_meta
class LoginForm(Form):
    name = simple.StringField(label="用户名", render_kw={"class": "form-control"})
    pwd = simple.PasswordField(label="密码", render_kw={"class": "form-control"})


# 2.根据LoginForm类去创建对象。会先执行FormMeta.__call__方法 -> LoginForm中的new去创建对象，init去初始化对象
form = LoginForm()
print(form.name)  # 类变量
print(form.pwd)  # 类变量

# 问题1：此时的LoginForm是由type or FormMeta创建？ 由FormMeta创建
"""
类中metaclass，自己类由metaclass定义的类来创建。
类继承某个类，如果父类中由metaclass，子类也是由父类中metaclass定义的类来创建。
"""












