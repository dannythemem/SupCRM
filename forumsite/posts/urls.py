from django.urls import path
from .views import index, PostsHome, AddPost

urlpatterns = [
    path('', PostsHome.as_view(), name='home'),
    path('add/', AddPost.as_view(), name='add'),
]