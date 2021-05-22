from django.contrib.auth import authenticate
from rest_framework import serializers
from ..models import User 

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password is not found.'
            )
        return {
            'message':'Ok good',
            'username': user.username
        }

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    def register(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user