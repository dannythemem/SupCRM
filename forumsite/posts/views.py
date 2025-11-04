from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from posts.forms import AddPostForm
from posts.models import Posts


# Create your views here.


class PostsHome(ListView):
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    extra_context = {'title': 'Главная страница'}

    def get_queryset(self):
        return Posts.published.all()

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


