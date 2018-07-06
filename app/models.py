from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class User_Base(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=250)
    is_active = models.CharField(default='Y', max_length=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.TextField()
    last_update_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.TextField()

    class Meta:
        ordering = ['username','last_update_date','last_updated_by']


class Role_Base(models.Model):
    role_name = models.CharField(max_length=20, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.TextField()
    last_update_date =models.DateTimeField(auto_now_add=True)
    last_updated_by = models.TextField()