from django.db import models

# Create your models here.


class Book(models.Model):
   name = models.CharField(max_length=64,null=True)

   def __str__(self):
       return self.name


class Publish(models.Model):
    name = models.CharField(max_length=64)



class User(models.Model):
    name = models.CharField(max_length=34,verbose_name="姓名")
    age = models.IntegerField(null=True)
    grade = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=64)



class Depart(models.Model):
    # 学院表
    id = models.IntegerField(primary_key=True,db_index=True,verbose_name="学院ID") # 学院ID
    name = models.CharField(max_length=255,verbose_name="学院名称")

    def __str__(self):
        return self.name
