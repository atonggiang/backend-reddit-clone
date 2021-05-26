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

class ProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=False)
    name = serializers.CharField(max_length=255, required=False)
    age = serializers.IntegerField(required=False)
    gender = serializers.CharField(max_length=1, required=False)

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    profile = ProfileSerializer(required=False)

class SubSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255, required=False)

class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField(max_length=255)

class CommentSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=255)