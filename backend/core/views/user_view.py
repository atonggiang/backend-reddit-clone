from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .. import models
from .. import serializers

@api_view(['POST'])
def login_authentication(request, *args, **kwargs):
    result = serializers.LoginSerializer(data=request.data)
    result.is_valid(raise_exception=True)
    
    user = models.User.objects.get(username=request.data['username'])
    refresh = RefreshToken.for_user(user)
    response = {
        'username': result.data['username'],
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    return Response(response, status=status.HTTP_200_OK)

@api_view(['POST'])
def register_user(request, *args, **kwargs):
    result = serializers.RegisterSerializer(data=request.data)
    result.register(request.data)
    response = {
        'username': request.data['username'],
        'password': request.data['password'],
    }
    return Response(response, status=status.HTTP_200_OK)