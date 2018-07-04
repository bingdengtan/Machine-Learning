from rest_framework import serializers
from app.models import User_Base, Role_Base


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Base
        fields = (
            'User_Name',
            'Email',
            'Creation_Date',
            'Created_By',
            'Last_Update_Date',
            'Last_Updated_By'
        )
        read_only_fields = ('id',)
    
