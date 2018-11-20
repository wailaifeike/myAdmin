import os

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KingAdmin.settings')
    import django
    django.setup()
    from app01 import models


    data_obj = models.CustomerInfo.objects.first()
    display = ["name", "contact_type", "contact", "source"]

    # for i in display:
    #     colum_obj = models.UserProfile._meta.get_field(i)
        #print(colum_obj)
        # if colum_obj.choices:
        #     colum_data = getattr(data_obj,'get_%s_display'%i)()
        #     print(colum_data)

