from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView

from posts.forms import AddPostForm
from posts.models import Posts, Like
from django.contrib.auth.models import User

# Create your views here.


class PostsHome(ListView):
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Главная страница'}

    def get_queryset(self):
        return (Posts.published
            .all()
            .annotate(
                num_likes=Count('posts_likes', filter=Q(posts_likes__reaction_type=Like.Status.LIKED)),
                num_dislikes=Count('posts_likes', filter=Q(posts_likes__reaction_type=Like.Status.DISLIKED)),
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

def react_post(request, post_id, status):
    if not request.user.is_authenticated:
        return redirect('users:login')
    user = request.user
    post = get_object_or_404(Posts, id=post_id)

    like, created = Like.objects.get_or_create(user=user, post=post)

    if status == 'like':
        if like.reaction_type == Like.Status.LIKED:
            like.delete()
        else:
            like.reaction_type = Like.Status.LIKED
            like.save()
    elif status == 'dislike':
        if like.reaction_type == Like.Status.DISLIKED:
            like.delete()
        else:
            like.reaction_type = Like.Status.DISLIKED
            like.save()
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect('home')

class AddPost(LoginRequiredMixin, CreateView):
    model = Posts
    form_class = AddPostForm
    template_name = 'posts/add_post.html'
    extra_context = {'title': 'Создать пост'}
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        f = form.save(commit=False)
        f.author = self.request.user
        return super().form_valid(form)

class PostView(LoginRequiredMixin, DetailView):
    model = Posts
    template_name = 'posts/post.html'
    context_object_name = 'post'


