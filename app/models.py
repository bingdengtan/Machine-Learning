from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class AuthUser(User):
    class Meta:
        managed = False
        proxy = True
        ordering = ('username',)


class User_Base(models.Model):
    User_Name = models.CharField(max_length=50)
    Email = models.EmailField()
    Is_Active = models.CharField(default='Y', max_length=2)
    Creation_Date = models.DateTimeField(auto_now_add=True)
    Created_By = models.TextField()
    Last_Update_Date = models.DateTimeField(auto_now_add=True)
    Last_Updated_By = models.TextField()

    class Meta:
        ordering = ['User_Name','Last_Update_Date','Last_Updated_By']


class Role_Base(models.Model):
    Role_Name = models.CharField(max_length=20)
    Creation_Date = models.DateTimeField(auto_now_add=True)
    Created_By = models.TextField()
    Last_Update_Date =models.DateTimeField(auto_now_add=True)
    Last_Updated_By = models.TextField() 