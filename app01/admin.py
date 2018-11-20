from django.contrib import admin

# Register your models here.

from Stark import stark

from app01 import models


class CustomerModel(stark.StarkModel):
    list_display = ["name","contact_type","contact","source"]
    list_filter = ["name"]


stark.sites.register(models.Student)
stark.sites.register(models.Teacher)
stark.sites.register(models.Exam)
stark.sites.register(models.CustomerInfo,CustomerModel)



admin.site.register(models.CustomerInfo)
admin.site.register(models.UserProfile)
admin.site.register(models.Course)
admin.site.register(models.Role)
admin.site.register(models.Menus)
