from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db import connection, reset_queries


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

def news(request):
    user_list = User.objects.all() #Список всех юзеров#
    # category_list = Article.category.
    selected = 0
    # selected1 = 0
    if request.method == "POST":
        # print(request.POST)
        selected = int(request.POST.get('author_filter'))
        if selected == 0:
            articles = Article.objects.all().order_by('-date')
        else:
            articles = Article.objects.filter(author=selected).order_by('-date')
        print(connection.queries)
    else:
        articles = Article.objects.all().order_by('-date')
    # if request.method == "POST":
    #     print(request.POST)
    #     selected1 = int(request.POST.get('category_filter'))
    #     if selected1 == 0:
    #         articles1 = Article.objects.all().order_by('-date')
    #     else:
    #         articles1 = Article.objects.filter(category=selected1).order_by('-date')
    #     print(connection.queries)
    # else:
    #     articles1 = Article.objects.all().order_by('-date')
    context = {'articles': articles, 'author_list': user_list,  'selected': selected} #'categories': category_list,'articles1': articles1,'selected1': selected1}

    # for category_single in category:
    #     print(Article.category.filter(author=user))
    # print(user_list)
    # articles = Article.objects.filter(author=request.user.id) #печатаем все статьи одного пользователя
    # context = {'article': articles}
    return render(request, 'news/news.html', context)

def index(request):
    #пример применения пользовательского менджера
    articles = Article.published.all()
    context={'today_articles': articles} #Это пример
    author_list = User.objects.all()
    selected = 0
    if request.method=="POST":
        # print(request.POST)
        selected = int(request.POST.get('author_filter'))
        if selected == 0:
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(author=selected)
        # print(connection.queries)
    else:
        articles = Article.objects.all()
    context = {'articles': articles, 'author_list': author_list, 'selected': selected }

    return render(request,'news/news.html',context)



def new_single (request):
    article = Article.objects.all().last()
    context = {'article': article}
    return render(request, 'news/new_single.html', context)


# def index(request):
#     article = Article.objects.all().first()
#     context = {'article':article}
#     return render(request,'news/index.html',context)

def detail(request, id):
    article = Article.objects.filter(id=id).first()
    print(article, type(article))
    context = {'article': article}
    # return HttpResponse(f'<h1>{article.title}</h1>')
    return render(request, 'news/new_single.html', context)
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

@login_required (login_url="/") #человек не аутентифицирован - отправляем на другую страницу
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            current_user = request.user
            if current_user.id !=None: #проверили что не аноним
                new_article = form.save(commit=False) #появится экземпляр новой статьи, но не будет сохранен в БД
                new_article.author = current_user
                new_article.save() #сохраняем в БД
                form.save_m2m()
                # form = ArticleForm() # обнуляем (чистим) форму
                return redirect('news_index')
    else:
        form = ArticleForm()
    return render(request,'news/create_article.html', {'form':form})
