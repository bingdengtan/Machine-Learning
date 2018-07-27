from rest_framework import serializers
from rest_framework_mongoengine import serializers as mongoserializers
from django.forms.models import model_to_dict
from django.utils import timezone
# from django.db.models import Q
from mongoengine.queryset.visitor import Q

from app.core.utils import encode_password
from app.models import User_Base, Role_Base, Project_Profile, Model_Profile
import json


class UserBaseSerializer(mongoserializers.DocumentSerializer):
    list_fields = ('id', 'username', 'is_active', 'email', 'roles', 'creation_date', 'created_by', 'last_updated_date', 'last_updated_by')

    class Meta:
        model = User_Base
        fields = ('username', 'is_active', 'email', 'password', 'creation_date', 'created_by', 'last_updated_date', 'last_updated_by',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        return User_Base.objects.create(**validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")

        instance.email = validated_data.get('email')
        instance.roles = validated_data.get('roles')
        instance.last_updated_by = request.user.username
        instance.last_updated_date = timezone.now()
        instance.save()
        return instance

    def is_user_exist(self, user):
        if not user.get('id') is None:
            query = (Q(username__iexact=user.get('username')) | Q(email__iexact=user.get('email'))) & Q(id__nin=[user.get('id')])
            users = self.Meta.model.objects(query)
        else:
            users = self.Meta.model.objects(
                Q(username__iexact=user.get('username')) | Q(email__iexact=user.get('email'))
            )
        return len(users) >= 1


class RoleBaseSerializer(mongoserializers.DocumentSerializer):
    class Meta:
        model = Role_Base
        fields = "__all__"
        read_only_fields = ('id',)

    def create(self, validated_data):
        return Role_Base.objects.create(**validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")

        instance.role_name = validated_data.get('role_name')
        instance.description = validated_data.get('description')
        instance.last_updated_by = request.user.username
        instance.last_updated_date = timezone.now()
        instance.save()
        return instance

    def is_role_exist(self, role):
        if not role.get('id') is None:
            roles = self.Meta.model.objects(
                Q(role_name__iexact=role.get('role_name')) & Q(id__nin=[role.get('id')])
            )
        else:
            roles = self.Meta.model.objects(role_name__iexact=role.get('role_name'))
        return len(roles) >= 1


class ProjectProfileSerializer(mongoserializers.DocumentSerializer):
    class Meta:
        model = Project_Profile
        fields = "__all__"
        read_only_fields = ('id',)

    def create(self, validated_data):
        return Project_Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")

        instance.name = validated_data.get('name')
        instance.description = validated_data.get('description')
        instance.last_updated_by = request.user.username
        instance.last_updated_date = timezone.now()
        instance.save()
        return instance

    def is_project_exist(self, project):
        if not project.get('id') is None:
            projects = self.Meta.model.objects(
                Q(name__iexact=project.get('name')) & Q(id__nin=[project.get('id')])
            )
        else:
            projects = self.Meta.model.objects(name__iexact=project.get('name'))
        return len(projects) >= 1


class ModelProfileSerializer(mongoserializers.DocumentSerializer):
    project_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Model_Profile
        fields = '__all__'
        read_only_fields = ('id', 'project')

    def get_project_name(self, obj):
        print(obj)
        obj_dict = obj.__dict__
        print(json.dumps(obj_dict))
        return 'AAA'

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")

        instance.name = validated_data.get('name')
        instance.project = validated_data.get('project')
        instance.description = validated_data.get('description')
        instance.last_updated_by = request.user.username
        instance.last_updated_date = timezone.now()
        instance.save()
        return instance

    def is_model_exist(self, model):
        if not model.get('id') is None:
            models = self.Meta.model.objects(
                Q(name__iexact=model.get('name')) & Q(id__nin=[model.get('id')])
            )
        else:
            models = self.Meta.model.objects(name__iexact=model.get('name'))
        return len(models) >= 1