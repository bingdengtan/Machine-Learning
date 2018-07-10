from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Role_Base(models.Model):
    role_name = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.TextField()
    last_updated_date =models.DateTimeField(auto_now_add=True)
    last_updated_by = models.TextField()


class User_Role(models.Model):
    user = models.ForeignKey('User_Base', on_delete=models.CASCADE)
    role = models.ForeignKey('Role_Base', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role',)

class User_Base(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=250, blank=True)
    is_active = models.CharField(default='Y', max_length=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.TextField()
    last_updated_date = models.DateTimeField(auto_now_add=True)
    last_updated_by = models.TextField()

    roles = models.ManyToManyField(Role_Base, through=User_Role)

    class Meta:
        ordering = ['username','last_updated_date','last_updated_by']