# Generated by Django 3.2.5 on 2021-09-13 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp_app', '0004_remove_admin_edit_form_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='edit_form_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
