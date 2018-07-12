from rest_framework import serializers
from rest_framework_mongoengine import serializers as mongoserializers
from datetime import datetime
from django.utils import timezone
#from django.db.models import Q
from mongoengine.queryset.visitor import Q

from app.core.utils import encode_password
from app.models import User_Base, Role_Base


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