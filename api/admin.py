from django.contrib import admin
from django.shortcuts import reverse

# Register your models here.

from api import models
from Stark import stark
from Stark.stark import StarkModel
from django.utils.safestring import mark_safe


class UserModel(StarkModel):
    display = ['id','name', 'age']
    display_links = ['name']

class BookModel(StarkModel):
    pass


stark.sites.register(models.User,UserModel)
stark.sites.register(models.Book,BookModel)
stark.sites.register(models.Publish)
stark.sites.register(models.Teacher)