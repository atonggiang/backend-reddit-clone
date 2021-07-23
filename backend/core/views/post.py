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
    profile = models.Profile.objects.create_profile(user, **profile_data)
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def edit_profile(request, *args, **kwargs):
    edit_content = serializers.ProfileSerializer(data=request.data)
    edit_content.is_valid()
    user = models.User.objects.get(username=request.user)
    user.profile = models.Profile(**edit_content.validated_data)
    user.profile.save()
    return Response({'message': 'success'}, status=status.HTTP_200_OK)


@api_view(['POST'])
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
    sub.members.add(user)
    return Response({'message': 'success',}, status=status.HTTP_200_OK)

@api_view(['POST'])
def join_sub(request, sub_name, *args, **kwargs):
    user = models.User.objects.get(username=request.user)
    sub = models.Sub.objects.get(name=sub_name)
    sub.members.add(user)
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def leave_sub(request, sub_name, *args, **kwargs):
    user = models.User.objects.get(username=request.user)
    sub = models.Sub.objects.get(name=sub_name)
    sub.members.remove(user)
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def comment_post(request, post_id, *args, **kwargs):
    comment_data = serializers.CommentSerializer(data=request.data)
    comment_data.is_valid()
    user = models.User.objects.get(username=request.user)
    post = models.Post.objects.get(id=post_id)
    comment = models.Comment(user=user, post=post, **comment_data.validated_data)
    comment.save()
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_post(request, sub_name, *args, **kwargs):
    user = models.User.objects.get(username=request.user)
    sub = models.Sub.objects.get(name=sub_name)
    post_data = serializers.PostSerializer(data=request.data)
    post_data.is_valid()
    post = models.Post(user=user, sub=sub, **post_data.validated_data)
    post.save()
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def upvote_post(request, post_id, *args, **kwargs):
    post = models.Post.objects.get(id=post_id)
    post.votes.up(request.user.id)
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def downvote_post(request, post_id, *args, **kwargs):
    post = models.Post.objects.get(id=post_id)
    post.votes.down(request.user.id)
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def del_vote_post(request, post_id, *args, **kwargs):
    post = models.Post.objects.get(id=post_id)
    post.votes.delete(request.user.id)
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def upvote_comment(request, comment_id, *args, **kwargs):
    comment = models.Comment.objects.get(id=comment_id)
    comment.votes.up(request.user.id)
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def downvote_comment(request, comment_id, *args, **kwargs):
    comment = models.Comment.objects.get(id=comment_id)
    comment.votes.down(request.user.id)
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def del_vote_comment(request, post_id, *args, **kwargs):
    comment = models.Post.objects.get(id=comment_id)
    comment.votes.delete(request.user.id)
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def reply_comment(request, comment_id, *args, **kwargs):
    user = models.User.objects.get(username=request.user)
    comment_parent = models.Comment.objects.get(id=comment_id)
    comment_data = serializers.CommentSerializer(data=request.data)
    comment_data.is_valid()
    comment = models.Comment(user=user, post=comment_parent.post, parent=comment_parent, **comment_data.validated_data)
    comment.save()
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def edit_post(request, post_id, *args, **kwargs):
    edit_content = serializers.PostSerializer(data=request.data)
    edit_content.is_valid()
    post = models.Post.objects.update_or_create({**edit_content.validated_data}, id=post_id)
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def edit_comment(request, comment_id, *args, **kwargs):
    edit_content = serializers.CommentSerializer(data=request.data)
    edit_content.is_valid()
    post = models.Comment.objects.update_or_create({**edit_content.validated_data}, id=comment_id)
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def edit_subdescription(request, sub_name, *args, **kwargs):
    edit_content = serializers.SubSerializer(data=request.data)
    edit_content.is_valid()
    post = models.Sub.objects.update_or_create({**edit_content.validated_data}, name=sub_name)
    return Response({'message': 'success'}, status=status.HTTP_200_OK)