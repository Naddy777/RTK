from django.shortcuts import render, HttpResponse
from django.http import HttpResponse
from .models import *
from .forms import *

def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print('Сообщение отправлено',form.cleaned_data)
        else:
            print(form.errors)
    else:
        form = ContactForm()
    context = {'form': form}
    return render(request,'users/contact_page.html', context)


# Create your views here.
def index (request):
    # article = Article.objects.all().first()
    # print('Автор новости', article.title, ':', article.author.account.gender)
    # context = {'article': article}
    # articles = Article.objects.filter(author=request.user.id) #печатаем все статьи одного пользователя
    # context = {'article': articles}
    user_acc = Account.objects.get(user=request.user)
    print(user_acc.birthdate, user_acc.gender)
    return render(request,'user/contact_page.html')