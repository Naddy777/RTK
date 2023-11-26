from django.shortcuts import render, HttpResponse
from django.http import HttpResponse
from .models import *


# Create your views here.
def index (request):
    # article = Article.objects.all().first()
    # print('Автор новости', article.title, ':', article.author.account.gender)
    # context = {'article': article}
    user_acc = Account.objects.get(user=request.user)
    print(user_acc.birthdate, user_acc.gender)
    return HttpResponse('Приложение юсер')