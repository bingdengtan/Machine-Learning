from rest_framework import serializers
from app.models import User_Base, Role_Base
from app.utils import encode_password


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Base
        fields = (
            'id',
            'username',
            'email',
            'password',
            'creation_date',
            'created_by',
            'last_update_date',
            'last_updated_by'
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        validated_data['password'] = encode_password(validated_data['password'])
        return User_Base.objects.create(**validated_data)
