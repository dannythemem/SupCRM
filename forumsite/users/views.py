from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

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


