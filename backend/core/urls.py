from django.urls import path, include
from . import views 

urlpatterns = [
    path('login/', views.login_authentication), #POST
    path('register/', views.register_user), #POST
    path('u/profile/', views.view_profile), #GET
    path('u/profile/edit/', views.edit_profile), #POST
    path('s/create/', views.create_sub), #POST
    path('s/<slug:sub_name>/join/', views.join_sub), #POST
    path('s/<slug:sub_name>/leave/', views.leave_sub), #POST
    path('p/<int:post_id>/comment/', views.comment_post), #POST
    path('c/<int:comment_id>/', views.view_comment), #GET
    path('s/all_sub/', views.all_sub), #GET
    path('s/<slug:sub_name>/', views.view_sub), #GET
    path('s/<slug:sub_name>/post/', views.create_post), #POST
    path('p/<int:post_id>/', views.view_post), #GET
    path('p/<int:post_id>/upvote/', views.upvote_post), #POST
    path('p/<int:post_id>/downvote/', views.downvote_post), #POST
    path('p/<int:post_id>/deletevote/', views.del_vote_post), #POST
    path('c/<int:comment_id>/upvote/', views.upvote_comment), #POST
    path('c/<int:comment_id>/downvote/', views.downvote_comment), #POST
    path('c/<int:comment_id>/deletevote/', views.del_vote_comment), #POST
    path('u/post_list/', views.post_list), #GET
    path('u/sub_list/', views.sub_list), #GET
    path('u/comment_list/', views.comment_list), #GET
    path('', views.home), #GET
    path('c/<int:comment_id>/reply/', views.reply_comment), #POST
    path('anonymous/s/<slug:sub_name>/', views.view_sub_anonymous), #GET
    path('anonymous/p/<int:post_id>/', views.view_post_anonymous), #GET
    path('anonymous/sub/all/', views.all_sub_anonymous), #GET
    path('p/<int:post_id>/edit/', views.edit_post), #POST
    path('c/<int:comment_id>/edit/', views.edit_comment), #POST
    path('s/<slug:sub_name>/edit/', views.edit_subdescription), #POST
    path('p/<int:post_id>/delete/', views.delete_post), #POST
    path('s/<slug:sub_name>/delete/', views.delete_sub), #POST
    path('p/search/',views.search_post) #GET
]