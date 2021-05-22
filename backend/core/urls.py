from django.urls import path, include
from . import views 

urlpatterns = [
    path('login/', views.login_authentication),
    path('register/', views.register_user),
]