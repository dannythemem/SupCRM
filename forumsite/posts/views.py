from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'posts/index.html', context={'title': 'Главная страница'})
