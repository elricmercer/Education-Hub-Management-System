# Generated by Django 3.2.5 on 2021-09-23 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp_app', '0013_auto_20210923_1509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyearnings',
            name='info',
        ),
    ]
