# Generated by Django 2.0.6 on 2018-07-05 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Role_Base',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Role_Name', models.CharField(max_length=20)),
                ('Creation_Date', models.DateTimeField(auto_now_add=True)),
                ('Created_By', models.TextField()),
                ('Last_Update_Date', models.DateTimeField(auto_now_add=True)),
                ('Last_Updated_By', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User_Base',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User_Name', models.CharField(max_length=50)),
                ('Email', models.EmailField(max_length=254)),
                ('Password', models.CharField(max_length=250)),
                ('Is_Active', models.CharField(default='Y', max_length=2)),
                ('Creation_Date', models.DateTimeField(auto_now_add=True)),
                ('Created_By', models.TextField()),
                ('Last_Update_Date', models.DateTimeField(auto_now_add=True)),
                ('Last_Updated_By', models.TextField()),
            ],
            options={
                'ordering': ['User_Name', 'Last_Update_Date', 'Last_Updated_By'],
            },
        ),
    ]
