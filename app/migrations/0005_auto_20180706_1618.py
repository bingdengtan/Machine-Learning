# Generated by Django 2.0.6 on 2018-07-06 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20180706_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_base',
            name='password',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]