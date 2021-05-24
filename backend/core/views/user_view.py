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
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def edit_profile(request, *args, **kwargs):
    edit_content = serializers.ProfileSerializer(data=request.data)
    edit_content.is_valid()
    user = models.User.objects.get(username=request.user)
    user.profile = models.Profile(**edit_content.validated_data)
    user.profile.save()
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def view_profile(request, *args, **kwargs):
    user = models.User.objects.get(username=request.user)
    profile_data = serializers.ProfileSerializer(user.profile)
    return Response(profile_data.data, status=status.HTTP_200_OK)

@api_view(['POST', 'PUT'])
def create_sub(request, *args, **kwargs):
    sub_data = serializers.SubSerializer(data=request.data)
    sub_data.is_valid()
    user = models.User.objects.get(username=request.user)
    if models.Sub.objects.filter(name=sub_data.validated_data['name']).exists():
        sub = models.Sub.objects.get(name=sub_data.validated_data['name'])
    else:
        sub = models.Sub(name=sub_data.validated_data['name'])
        sub.save()
    sub.mods.add(user)
    return Response({'message': 'success',}, status=status.HTTP_200_OK)
