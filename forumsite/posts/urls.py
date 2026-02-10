from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostsHome.as_view(), name='home'),
    path('add/', views.AddPost.as_view(), name='add'),
    path('posts/<int:post_id>/<str:status>/', views.react_post, name='react' ),
    path('comments/<int:pk>/<slug:slug>', views.CommentsView.as_view(), name='comments'),
]