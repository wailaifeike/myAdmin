# Generated by Django 2.1.3 on 2018-11-18 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_user_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='grade',
            field=models.IntegerField(null=True),
        ),
    ]
