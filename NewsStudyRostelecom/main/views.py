from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import News
def index (request):
    value = -10
    n1 = News('Новость 1', 'Текст 1', '07.11.23')
    n2 = News('Новость 2', 'Текст 1', '07.11.23')
    l = [n1, n2]
    m = ['раз', 'два', 'три']
    context = {'title': 'Мой сайт',
            'Header1': 'Заголовок страницы',
               'value': value,
               'numbers': l,
               'numbers2': m,
               }
    return render(request, 'main/index.html', context)
def contacts (request):
    return HttpResponse('<h1> Контакты </h1>')
def about (request):
    return HttpResponse('<h1> О нас </h1>')
def sidebar (request):
    return render(request, 'main/sidebar.html')

def test_page (request):
    return render(request, 'main/test_page.html')