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
    comment = models.Comment(user=user, post=post, content=comment_data.validated_data['content'])
    comment.save()
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def view_comment(request, comment_id, *args, **kwargs):
    comment = models.Comment.objects.get(id=comment_id)
    return Response({"username":comment.user.username, "content":comment.content}, status=status.HTTP_200_OK)

@api_view(['GET'])
def view_sub(request, sub_name, *args, **kwargs):
    sub = models.Sub.objects.get(name=sub_name)
    posts = sub.post_set.all()
    posts_data = []
    for post in posts:
        posts_data.append({
            "author":post.user.username,
            "title": post.title,
            "content": post.content,
            "total_vote_count": post.votes.count(),
            "upvote_count": post.votes.count(0),
            "downvote_count": post.votes.count(1),
            "total_comment":post.comment_set.count(),
            "link":post.get_absolute_url()
            })
    return Response({
        "name":sub.name, 
        "description":sub.description,
        "members": sub.members.count(),
        "posts": posts_data
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
def view_post(request, post_id, *args, **kwargs):
    post = models.Post.objects.get(id=post_id)
    comments = post.comment_set.all()
    comments_data = []
    for comment in comments:
        comments_data.append({
            "author": comment.user.username,
            "content": comment.content,
            "total_vote_count": comment.votes.count(),
            "upvote_count": comment.votes.count(0),
            "downvote_count": comment.votes.count(1),
            "link": comment.get_absolute_url(),
            })
    return Response({
        "author":post.user.username,
        "title":post.title, 
        "content":post.content,
        "total_vote_count": post.votes.count(),
        "upvote_count": post.votes.count(0),
        "downvote_count": post.votes.count(1),
        "total_comment":post.comment_set.count(),
        "comments": comments_data,
        }, status=status.HTTP_200_OK)

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
def upvote_comment(request, comment_id, *args, **kwargs):
    comment = models.Comment.objects.get(id=comment_id)
    comment.votes.up(request.user.id)
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def downvote_comment(request, comment_id, *args, **kwargs):
    comment = models.Comment.objects.get(id=comment_id)
    comment.votes.down(request.user.id)
    return Response({'message': 'success'}, status=status.HTTP_200_OK)

@api_view(['GET'])
def sub_list(request, *args, **kwargs):
    user = models.User.objects.get(username=request.user)
    subs = user.subs_join.all()
    subs_data = []
    for sub in subs:
        subs_data.append({
            "name": sub.name,
            "link":sub.get_absolute_url()
            })
    return Response({
        "subs": subs_data
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
def post_list(request, *args, **kwargs):
    user = models.User.objects.get(username=request.user)
    posts = user.post_set.all()
    posts_data = []
    for post in posts:
        posts_data.append({
            "author":post.user.username,
            "title": post.title,
            "content": post.content,
            "total_vote_count": post.votes.count(),
            "upvote_count": post.votes.count(0),
            "downvote_count": post.votes.count(1),
            "total_comment":post.comment_set.count(),
            "link":post.get_absolute_url()
            })
    return Response({
        "posts": posts_data
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
def comment_list(request, *args, **kwargs):
    user = models.User.objects.get(username=request.user)
    comments = user.comment_set.all()
    comments_data = []
    for comment in comments:
        comments_data.append({
            "author": comment.user.username,
            "content": comment.content,
            "total_vote_count": comment.votes.count(),
            "upvote_count": comment.votes.count(0),
            "downvote_count": comment.votes.count(1),
            "link": comment.get_absolute_url(),
            })
    return Response({
        "comments": comments_data
        }, status=status.HTTP_200_OK)

@api_view(['GET'])
def home(request, *args, **kwargs):
    user = models.User.objects.get(username=request.user)
    subs = user.subs_join.all()
    subs_data = []
    for sub in subs:
        posts = sub.post_set.all()
        posts_data = []
        for post in posts:
            posts_data.append({
                "author":post.user.username,
                "title": post.title,
                "content": post.content,
                "total_vote_count": post.votes.count(),
                "upvote_count": post.votes.count(0),
                "downvote_count": post.votes.count(1),
                "total_comment":post.comment_set.count(),
                "link":post.get_absolute_url()
                })
        subs_data.append({
            "name":sub.name,
            "posts":posts_data
        })
    return Response({
        "data":subs_data, 
        }, status=status.HTTP_200_OK)