# Generated by Django 2.0.6 on 2018-07-09 02:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20180706_1618'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user_base',
            options={'ordering': ['username', 'last_updated_date', 'last_updated_by']},
        ),
        migrations.RenameField(
            model_name='role_base',
            old_name='last_update_date',
            new_name='last_updated_date',
        ),
        migrations.RenameField(
            model_name='user_base',
            old_name='last_update_date',
            new_name='last_updated_date',
        ),
    ]