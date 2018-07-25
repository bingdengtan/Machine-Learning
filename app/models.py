from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from mongoengine import Document, EmbeddedDocument, fields, ListField, ReferenceField

# Create your models here.


class Role_Base(Document):
    role_name = fields.StringField(required=True, unique=True)
    description = fields.StringField(required=False, null=True)
    creation_date = fields.DateTimeField(default=timezone.now(), null=True)
    created_by = fields.StringField()
    last_updated_date = fields.DateTimeField(default=timezone.now(), null=True)
    last_updated_by = fields.StringField()


class User_Base(Document):
    username = fields.StringField(required=True, unique=True)
    email = fields.StringField(required=True)
    password = fields.StringField(required=False, unique=False, null=True)
    is_active = fields.StringField(default='Y')
    creation_date = fields.DateTimeField(default=timezone.now())
    created_by = fields.StringField()
    last_updated_date = fields.DateTimeField(default=timezone.now())
    last_updated_by = fields.StringField()

    roles = ListField(ReferenceField(Role_Base))


class Project_Profile(Document):
    name = fields.StringField(required=True, unique=True)
    description = fields.StringField(required=False, null=True)
    creation_date = fields.DateTimeField(default=timezone.now(), null=True)
    created_by = fields.StringField()
    last_updated_date = fields.DateTimeField(default=timezone.now(), null=True)
    last_updated_by = fields.StringField()   


class Model_Profile(Document):
    name = fields.StringField(required=True, unique=True)
    path = fields.StringField(required=True)
    description = fields.StringField(required=False, null=True)
    creation_date = fields.DateTimeField(default=timezone.now(), null=True)
    created_by = fields.StringField()
    last_updated_date = fields.DateTimeField(default=timezone.now(), null=True)
    last_updated_by = fields.StringField()

    project = ReferenceField(Project_Profile)
