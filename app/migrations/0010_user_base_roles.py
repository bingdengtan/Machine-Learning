# Generated by Django 2.0.6 on 2018-07-10 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20180709_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_base',
            name='roles',
            field=models.ManyToManyField(through='app.User_Role', to='app.Role_Base'),
        ),
    ]
