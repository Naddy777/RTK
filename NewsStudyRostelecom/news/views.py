from django.shortcuts import render
from .models import *
from django.http import HttpResponse

# Create your views here.
# Вытаскиваем первую новость, автора, заголовок
# def news (request):
#     article = Article.objects.all().first()
#     print('Автор новости', article.title,':', article.author.username)
#     context = {'article':article}
#     return render(request,'news/news.html',context)

# Вытаскиваем статьи пользователя
# def news (request):
#     articles = Article.objects.filter(author=request.user.id)
#     print(articles)
#     context = {'article':articles}
#     return render(request,'news/news.html',context)

# Выводим теги через новость
# def news (request):
#     articles = Article.objects.get(author=2)
#     print(articles.tags.all())
#     context = {'article': articles}
#     return render(request, 'news/news.html', context)

# Выводим новость через теги
# def news (request):
#     articles = Article.objects.get(author=2)
#     print(articles.tags.all())
#     tag = Tag.objects.filter(title='Ветер')[0]
#     tagged_news = Article.objects.filter(tags=tag)
#     print(tagged_news)
#     user_list = User.objects.all() #Список всех юзеров#
#     for user in user_list:
#         print(Article.objects.filter(author=user))
#     print(user_list)
#     context = {'article': articles}
#     return render(request, 'news/news.html', context)

def news (request):
    articles = Article.objects.all()
    user_list = User.objects.all() #Список всех юзеров#
    for user in user_list:
        print(Article.objects.filter(author=user))
    print(user_list)
    context = {'articles': articles, 'author_list': user_list }
    return render(request, 'news/news.html', context)

def index(request):
    #пример применения пользовательского менджера
    articles = Article.published.all()
    context={'today_articles': articles}
    author_list = User.objects.all()
    selected = 0
    if request.method=="POST":
        print(request.POST)
        selected = int(request.POST.get('author_filter'))
        if selected == 0:
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(author=selected)
        print(connection.queries)
    else:
        articles = Article.objects.all()
    context = {'articles': articles, 'author_list': author_list, 'selected': selected }

    return render(request,'news/news.html',context)



def new_single (request):
    return render(request, 'news/new_single.html')


# def index(request):
#     article = Article.objects.all().first()
#     context = {'article':article}
#     return render(request,'news/index.html',context)

def detail(request,id):
    article = Article.objects.filter(id=id).first()
    print(article, type(article))
    return HttpResponse(f'<h1>{article.title}</h1>')
    # return render(request, 'news/new_single.html')
#Пример создания новостей#
# def detail(request,id):
#     author = User.objects.get(id=request.user.id)
#     article = Article(author=author, title='Заголовок', anouncement='Анонс', text='текст')
#     article.save()
#     return HttpResponse(f'<h1>{article.title}</h1>')

#Пример вывода всех новостей (итерировать по объектам QuerySet)#
# def detail(request,id):
#     articles = Article.objects.all()
#     s=''
#     for article in articles:
#         s+=f'<h1>{article.title}</h1><br>'
#     return HttpResponse(s)

# user_list = User.objects.all()
#     for user in user_list:
#         print(Article.objects.filter(author=user))
#     print(user_list)