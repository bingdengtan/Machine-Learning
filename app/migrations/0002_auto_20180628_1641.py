# Generated by Django 2.0.6 on 2018-06-28 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user_base',
            options={'ordering': ('User_Name',)},
        ),
        migrations.AlterField(
            model_name='role_base',
            name='Creation_Date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user_base',
            name='Creation_Date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
