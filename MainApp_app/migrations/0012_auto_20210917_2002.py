# Generated by Django 3.2.5 on 2021-09-17 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp_app', '0011_contactus_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='end_time',
        ),
        migrations.AddField(
            model_name='attendance',
            name='duration',
            field=models.CharField(default='1 hr', max_length=15),
            preserve_default=False,
        ),
    ]
