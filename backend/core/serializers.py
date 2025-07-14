from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from .models import MyUser


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email',
                  'password', 'first_name', 'last_name']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class PublicUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
