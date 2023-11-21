from django.shortcuts import render, HttpResponse
from django.http import HttpResponse

# Create your views here.
def index (request):
    article = Article.objects.all().first()
    print('Автор новости', article.title, ':', article.author.account.gender)
    context = {'article': article}

    return HttpResponse('Приложение юсер')