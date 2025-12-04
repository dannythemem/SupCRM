from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/<str:username>/', views.ProfileUser.as_view(), name='profile'),
    path('profile/<str:username>/posts/', views.UsersPosts.as_view(), name='my_posts'),
    path('profile/<str:username>/liked_posts/', views.UsersLikedPosts.as_view(), name='liked_posts'),
    path('profile/<str:username>/disliked_posts/', views.UsersDislikedPosts.as_view(), name='disliked_posts'),

]