from rest_framework import serializers
from datetime import datetime
from django.utils import timezone
from django.db.models import Q

from app.core.utils import encode_password
from app.models import User_Base, Role_Base, User_Role


class UserBaseSerializer(serializers.ModelSerializer):
    list_fields = ('id', 'username', 'is_active', 'email', 'roles', 'creation_date', 'created_by', 'last_updated_date', 'last_updated_by')

    class Meta:
        model = User_Base
        fields = ('id', 'username', 'is_active', 'email', 'password', 'creation_date', 'created_by', 'last_updated_date', 'last_updated_by',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        return User_Base.objects.create(**validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")

        instance.email = validated_data.get('email')
        instance.last_updated_by = request.user.username
        instance.last_updated_date = timezone.now()
        instance.save()
        return instance

    def is_user_exist(self, user):
        if not user.get('id') is None:
            users = self.Meta.model.objects.filter(
                Q(username__iexact=user.get('username')) | Q(email__iexact=user.get('email')),
                ~Q(id__in=[user.get('id')])
            )
        else:
            users = self.Meta.model.objects.filter(
                Q(username__iexact=user.get('username')) | Q(email__iexact=user.get('email'))
            )
        return len(users) >= 1


class RoleBaseSerializer(serializers.ModelSerializer):
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
            roles = self.Meta.model.objects.filter(
                Q(role_name__iexact=role.get('role_name')),
                ~Q(id__in=[role.get('id')])
            )
        else:
            roles = self.Meta.model.objects.filter(
                Q(role_name__iexact=role.get('role_name'))
            )
        return len(roles) >= 1

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Role
        fields = "__all__"

    def create(self, validated_data):
        return User_Role.objects.create(**validated_data)

    def remove_user_roles_by_user_id(self, user_id):
        self.Meta.model.objects.filter(user=user_id).delete();
