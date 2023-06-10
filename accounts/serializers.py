from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from accounts.models import UserAccount
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import Packages
# from django.contrib.auth import get_user_model
# User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = UserAccount
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'password']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['id'] = str(user.id)

        return token


class PackageSerializer(serializers.ModelSerializer):
    """Serializer for Site Configuration"""
    class Meta:
        model = Packages
        fields = "__all__"