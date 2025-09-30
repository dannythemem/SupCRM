from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from posts.forms import AddPostForm
from posts.models import Posts


# Create your views here.

def index(request):
    return render(request, 'posts/index.html', context={'title': 'Главная страница'})

class PostsHome(ListView):
    template_name = 'posts/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'

    def get_queryset(self):
        return Posts.published.all()

class AddPost(CreateView):
    model = Posts
    form_class = AddPostForm
    template_name = 'posts/add_post.html'
    extra_context = {'title': 'Создать пост'}
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        f = form.save(commit=False)
        return super().form_valid(form)
