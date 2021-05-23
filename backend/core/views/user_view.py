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
        'token': str(refresh.access_token),
    }
    return Response(response, status=status.HTTP_200_OK)

@api_view(['POST'])
def register_user(request, *args, **kwargs):
    register_data = serializers.RegisterSerializer(data=request.data)
    register_data.is_valid()
    profile_data = {}
    if 'profile' in register_data.validated_data:
        profile_data = register_data.validated_data.pop('profile')
    user = models.User.objects.create_user(**register_data.validated_data)
    profile = models.Profile.object.create_profile(user, **profile_data)
    response = {
        'message': 'done',
    }
    return Response(response, status=status.HTTP_200_OK)

@api_view(['POST'])
def edit_profile(request, *args, **kwargs):
    edit_content = serializers.ProfileSerializer(data=request.data)
    edit_content.is_valid()
    user = models.User.objects.get(username=request.user)
    user.profile = models.Profile(**edit_content.validated_data)
    user.profile.save()
    response = {
        'message': 'done',
    }
    return Response(response, status=status.HTTP_200_OK)

@api_view(['GET'])
def view_profile(request, *args, **kwargs):
    user = models.User.objects.get(username=request.user)
    profile_data = serializers.ProfileSerializer(user.profile)
    return Response(profile_data.data, status=status.HTTP_200_OK)

