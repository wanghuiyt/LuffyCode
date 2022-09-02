MVT: model view template  
django-admin startproject 项目名  
python manage.py runserver ip:port  # 启动项目  
python manage.py startapp  # 创建app

URL控制器  
视图函数  
模板  
ORM  
    -- object relation mapping   
    -- 类：sql语句table表  
    -- 类成员变量：table表中的字段、类型和约束  
    -- 类对象：sql表的表记录

    -- 配置数据连接信息
    -- 在models.py中定义模型类
    -- 生成数据迁移文件并执行迁移文件[注意：数据迁移是一个独立的功能，这个功能在其他web框架未必和ORM一样]
    -- 通过模型类对象提供的方法或属性完成数据表的增删改查操作

    -- 迁移
        -- python manage.py makemigrations
        -- python manage.py migrate

    -- queryset ORM中的类型，类似于列表，
