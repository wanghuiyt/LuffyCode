from django.db import models

# Create your models here.
"""
class table Student
    id int primary key
    name varchar(32) unique
    birth_day date
"""


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, unique=True)
    age = models.IntegerField(default=0)
    birth_day = models.DateField()

    class Meta:
        db_table = 'tb_student'

    def __str__(self):
        return self.name
