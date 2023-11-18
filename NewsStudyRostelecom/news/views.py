from django.shortcuts import render
from .models import *
from django.http import HttpResponse

# Create your views here.
def news_index (request):
    return render(request, 'news/news_index.html')

def news_news (request):
    return render(request, 'news/news_news.html')


def index(request):
    article = Article.objects.all().first()
    context = {'article':article}
    return render(request,'news/index.html',context)

def detail(request,id):
    article = Article.objects.filter(id=id).first()
    print(article,type(article))
    return HttpResponse(f'<h1>{article.title}</h1>')