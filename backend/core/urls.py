from django.urls import path, include
from . import views 

urlpatterns = [
    path('login/', views.login_authentication),
    path('register/', views.register_user),
    path('u/profile/', views.view_profile),
    path('u/profile/edit/', views.edit_profile),
    path('sub/create/', views.create_sub),
    path('s/sub/<slug:sub_name>/join/', views.join_sub),
    path('s/sub/<slug:sub_name>/leave/', views.leave_sub),
    path('p/<int:post_id>/comment/', views.comment_post),
    path('c/<int:comment_id>/', views.view_comment),
    path('s/<slug:sub_name>/', views.view_sub),
    path('p/<int:post_id>/', views.view_post),
    path('p/<int:post_id>/upvote/', views.upvote_post),
    path('p/<int:post_id>/downvote/', views.downvote_post),
    path('c/<int:comment_id>/upvote/', views.upvote_comment),
    path('c/<int:comment_id>/downvote/', views.downvote_comment),
    path('u/post_list/', views.post_list),
    path('u/sub_list/', views.sub_list),
    path('u/comment_list/', views.comment_list),
    path('', views.home),
]