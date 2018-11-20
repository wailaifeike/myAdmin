from django.conf.urls import url
from django.http import HttpResponse
from django.shortcuts import render,reverse,redirect
from django.utils.safestring import mark_safe
from django.forms import ModelForm
import datetime


class StarkModel(object):

    list_display = ["__str__"]

    display_links = []

    list_filter = []

    def check_box(self, obj=None,header=False):
        if header:
            return mark_safe("<input type='checkbox' class='choice'/>" )
        return mark_safe("<input  type='checkbox' class='choice_item'/>" )

    def __init__(self,model,site):
        self.model = model
        self.site = site

    def edit(self, obj=None,header=False):
        if header:
            return "操作"

        # print("_url", _url)
        return mark_safe("<a href='%s'>编辑</a>" % self.get_change_url(obj))

    def delete_view(self, obj=None,header=False):
        if header:
            return "删除"
        app_name = self.model._meta.app_label
        model_name = self.model._meta.model_name
        _url = reverse("%s_%s_delete" % (app_name, model_name), args=(obj.pk,))  # api_user_list
        print("_url", _url)
        return mark_safe("<a href='%s'>删除</a>" % _url)


    def get_change_url(self,obj):
        app_name = self.model._meta.app_label
        model_name = self.model._meta.model_name
        _url = reverse("%s_%s_change" % (app_name, model_name), args=(obj.pk,))  # api_user_list
        return _url

    def get_add_url(self):
        app_name = self.model._meta.app_label
        model_name = self.model._meta.model_name
        _url = reverse("%s_%s_add" % (app_name, model_name))  # api_user_list
        return _url
    def get_delete_url(self,obj):
        app_name = self.model._meta.app_label
        model_name = self.model._meta.model_name
        _url = reverse("%s_%s_delete" % (app_name, model_name), args=(obj.pk,))  # api_user_list
        return _url

    def get_list_url(self):
        app_name = self.model._meta.app_label
        model_name = self.model._meta.model_name
        _url = reverse("%s_%s_list" % (app_name, model_name))  # api_user_list
        return _url

    @property
    def get_urls2(self):
        return self.getOptions(), None, None

    def getOptions(self):
        app_name = self.model._meta.app_label
        model_name = self.model._meta.model_name
        option_list = []
        option_list.append(url(r'^add/$', self.add,name='%s_%s_add'%(app_name,model_name)))
        option_list.append(url(r'^(\d+)/delete/$', self.delete,name='%s_%s_delete'%(app_name,model_name)))
        option_list.append(url(r'^(\d+)/change/$', self.change,name='%s_%s_change'%(app_name,model_name)))
        option_list.append(url(r'^$', self.list,name='%s_%s_list'%(app_name,model_name)))
        return option_list



    def new_display(self):
        temp = []
        temp.append(StarkModel.check_box)
        temp.extend(self.list_display)
        if not self.display_links:
            temp.append(StarkModel.edit)
        temp.append(StarkModel.delete_view)
        return temp



    def add(self, request):

        class ModelFormDemo(ModelForm):
            class Meta:
                model = self.model
                fields = "__all__"
                labels = {
                    ""
                }

        if request.method == "POST":
            print(request.POST.get("name"))
            form_obj = ModelFormDemo(request.POST)
            if form_obj.is_valid():
                form_obj.save()
                return redirect(self.get_list_url())

            return render(request, "stark/add.html", {"form_obj":form_obj})



        form_obj = ModelFormDemo()

        return render(request,'stark/add.html',{"form_obj":form_obj})


    def get_list_filter(self,filter_column):

        # print("column obj:", column_obj)
        try:
            column_obj = self.model._meta.get_field(filter_column)
            print(column_obj,"_-------")
            filter_ele = "<select name='%s'>" % filter_column
            for choice in column_obj.get_choices():
                selected = ''
                if filter_column in self.list_filter:  # 当前字段被过滤了
                    # print("filter_column", choice,
                    #       type(admin_class.filter_condtions.get(filter_column)),
                    #       admin_class.filter_condtions.get(filter_column))
                    if str(choice[0]) == self.model.filter_condtions.get(filter_column):  # 当前值被选中了
                        selected = 'selected'
                        print('selected......')

                option = "<option value='%s' %s>%s</option>" % (choice[0], selected, choice[1])
                filter_ele += option
        except AttributeError as e:
            print("err", e)
            filter_ele = "<select name='%s__gte'>" % filter_column
            if column_obj.get_internal_type() in ('DateField', 'DateTimeField'):
                time_obj = datetime.datetime.now()
                time_list = [
                    ['', '------'],
                    [time_obj, 'Today'],
                    [time_obj - datetime.timedelta(7), '七天内'],
                    [time_obj.replace(day=1), '本月'],
                    [time_obj - datetime.timedelta(90), '三个月内'],
                    [time_obj.replace(month=1, day=1), 'YearToDay(YTD)'],
                    ['', 'ALL'],
                ]

                for i in time_list:
                    selected = ''
                    time_to_str = '' if not i[0] else "%s-%s-%s" % (i[0].year, i[0].month, i[0].day)
                    if "%s__gte" % filter_column in self.model.filter_condtions:  # 当前字段被过滤了
                        print('-------------gte')
                        if time_to_str == self.model.filter_condtions.get("%s__gte" % filter_column):  # 当前值被选中了
                            selected = 'selected'
                    option = "<option value='%s' %s>%s</option>" % \
                             (time_to_str, selected, i[1])
                    filter_ele += option

        filter_ele += "</select>"
        return mark_safe(filter_ele)


    def list(self,request):
        datalist = self.model.objects.all()
        print("self.display", self.list_display)
        data_array = []

        head_list = []

        for fields in self.new_display():  # [checkbox,'__str__','操作',edit]
            if callable(fields):
                val= fields(self,header=True)
                head_list.append(val)
            else:
                if fields == "__str__":
                    head_list.append(self.model._meta.model_name.upper())
                else:
                    fields_obj = self.model._meta.get_field(fields)
                    print(fields_obj.verbose_name)
                    head_list.append(fields_obj.verbose_name)



        print("display",self.list_display)
        for obj in datalist:                    #data  [obj,obj]  #"[name","contact_type","contact","source"] 其中含有choices字段
            temp = []
            for field in self.new_display():          #['name','age',edit]  field ==='name'
                if callable(field):             #如何传来的是函数，就调用方法得到返回值
                    val = field(self,obj)
                else:

                    if field in self.display_links:
                        val = getattr(obj,field)
                        val = mark_safe("<a href='%s'>%s</a>"%(self.get_change_url(obj),val))
                    else:
                        # print("contact_type",self.model._meta.get_field("contact_type"))
                        try:
                            column_obj = self.model._meta.get_field(field)
                            if column_obj.choices:
                                column_data = getattr(obj, 'get_%s_display' % field)()
                                filter_str = self.get_list_filter(field)
                                print(filter_str)
                                val = column_data
                            else:
                                val = getattr(obj,field)
                        except Exception:
                                print("filter_str")
                                val = getattr(obj,field)
                temp.append(val)
            data_array.append(temp)

        return render(request,'stark/list.html',{"data":data_array,"head_list":head_list,"url":self.get_add_url(),"filter_str":filter_str})


    def delete(self,request,id):
        list_url = self.get_list_url()
        if request.method == "POST":
            print("id",id)
            self.model.objects.filter(pk=id).delete()
            return redirect(list_url)

        return render(request, "stark/delete.html", locals())

    def change(self,request,id):

        edit_obj = self.model.objects.filter(pk=id).first()
        class ModelFormDemo(ModelForm):
            class Meta:
                model = self.model
                fields = "__all__"
                labels = {
                    ""
                }

        if request.method == "POST":
            print(request.POST.get("name"))
            form_obj = ModelFormDemo(request.POST,instance=edit_obj)
            if form_obj.is_valid():
                form_obj.save()
                return redirect(self.get_list_url())

            return render(request, "stark/change.html", {"form_obj":form_obj})



        form_obj = ModelFormDemo(instance=edit_obj)

        return render(request,'stark/change.html',{"form_obj":form_obj})




class StarkAdmin(object):
    def __init__(self):
        self._registry = {}

    def register(self, model_class, admin_class=None, **options):

        """注册admin表"""

        # print("register",model_class,admin_class)
        app_name = model_class._meta.app_label
        # model_name = model_class._meta.model_name
        if not admin_class:  # 为了避免多个model共享同一个BaseKingAdmin内存对象
            admin_class = StarkModel
        # else:
        #     admin_class = admin_class()

        #admin_class.model = model_class  # 把model_class赋值给了admin_class
        #
        # if app_name not in self._registry:
        #     self._registry[model_class] = {}
        self._registry[model_class] = admin_class(model_class,self)

    @property
    def urls(self):
        return self.get_urls(), None,None

    def get_urls(self):

        urlpatterns = []
        for model_class,admin_class_obj in self._registry.items():
            app_label = model_class._meta.app_label
            model_name = model_class._meta.model_name
            urlpatterns.append(url(r'^%s/%s/'%(app_label,model_name),admin_class_obj.get_urls2))
        return urlpatterns


sites = StarkAdmin()
