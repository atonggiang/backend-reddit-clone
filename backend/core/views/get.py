from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .. import models
from .. import serializers

@api_view(['GET'])
def sub_list(request, *args, **kwargs):
    user = models.User.objects.get(username=request.user)
    subs = user.subs_join.all()
    subs_data = []
    for sub in subs:
        data = sub.info(user, [])
        data.pop('description')
        data.pop('members')
        data.pop('join_status')
        data.pop('posts')
        subs_data.append(data)
    return Response(subs_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def all_sub(request, *args, **kwargs):
    user = models.User.objects.get(username=request.user)
    subs = models.Sub.objects.all()
    subs_data = []
    for sub in subs:
        data = sub.info(user, [])
        data.pop('description')
        data.pop('members')
        data.pop('posts')
        subs_data.append(data)
    return Response(subs_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def comment_list(request, *args, **kwargs):
    user = models.User.objects.get(username=request.user)
    comments = user.comment_set.all()
    comments_data = []
    for comment in comments:
        data = comment.info(user)
        if "children_comment" in data:
            data.pop("children_comment")
        comments_data.append(data)
    return Response(comments_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def view_profile(request, *args, **kwargs):
    user = models.User.objects.get(username=request.user)
    profile_data = serializers.ProfileSerializer(user.profile)
    return Response(profile_data.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_comment(request, comment_id, *args, **kwargs):
    comment = models.Comment.objects.get(id=comment_id)
    return Response({"username":comment.user.username, "content":comment.content}, status=status.HTTP_200_OK)

@api_view(['GET'])
def view_sub(request, sub_name, *args, **kwargs):
    user = models.User.objects.get(username=request.user)
    sub = models.Sub.objects.get(name=sub_name)
    posts = sub.post_set.all()
    posts_data = []
    for post in posts:
        data = post.info(user, [])
        data.pop("comments")
        posts_data.append(data)
    return Response(sub.info(user, posts_data), status=status.HTTP_200_OK)

@api_view(['GET'])
def view_post(request, post_id, *args, **kwargs):
    user = models.User.objects.get(username=request.user)
    post = models.Post.objects.get(id=post_id)
    comments = post.comment_set.all()
    comments_data = []
    for comment in comments:
        if comment.parent is None:
            comments_data.append(comment.info(user))
    return Response(post.info(user, comments_data), status=status.HTTP_200_OK)

@api_view(['GET'])
def home(request, *args, **kwargs):
    user = models.User.objects.get(username=request.user)
    subs = user.subs_join.all()
    subs_data = []
    for sub in subs:
        posts = sub.post_set.all()
        posts_data = []
        for post in posts:
            data = post.info(user, [])
            data.pop('comments')
            posts_data.append(data)
        data = sub.info(user, posts_data)
        data.pop('description')
        data.pop('members')
        data.pop('join_status')
        subs_data.append(data)
    return Response(subs_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def post_list(request, *args, **kwargs):
    user = models.User.objects.get(username=request.user)
    posts = user.post_set.all()
    posts_data = []
    for post in posts:
        data = post.info(user, [])
        data.pop('comments')
        posts_data.append(data)
    return Response(posts_data, status=status.HTTP_200_OK)