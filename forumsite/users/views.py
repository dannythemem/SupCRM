from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from posts.models import Posts
from users.forms import LoginUserForm, RegisterUserForm


# Create your views here.

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}

class RegisterUser(generic.CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')

class ProfileUser(generic.DetailView):
    model = get_user_model()
    template_name = 'users/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        username = self.kwargs.get('username')
        context['viewed_user'] = get_object_or_404(get_user_model(), username=username)
        context["title"] = user.username
        return context


class UsersPosts(generic.ListView):
    template_name = 'users/my_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(get_user_model(), username=username)
        return Posts.objects.filter(author=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['viewed_user'] = get_object_or_404(get_user_model(), username=username)
        context['title'] = get_object_or_404(get_user_model(), username=username).username
        return context

