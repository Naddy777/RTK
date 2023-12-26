from django.shortcuts import render
from django.http import HttpResponse
from .models import News, Product
from news.models import Article
from django.db.models import Count, Avg
from django.contrib.auth.models import User
import json
import git
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


def index (request):
    all_news = Article.objects.all().values('author','title')
    article = Article.objects.all().last()
    # for a in all_news:
    #     print(a['author'], a['title'])
    context = {'articles': all_news, 'article': article}
#     all_news = Article.objects.all().values_list('author','title')
#     for a in all_news:
#         print(a)
    # По старому:
    # article = Article.objects.get(id=1)
    # print(article.author.username)

    # Через select_related:
    # article = Article.objects.select_related('author').get(id=1)
    # print(article.author.username)

    # Через prefetch_related М2М:
    # articles= Article.objects.prefetch_related('tags').all()
    # print(articles)

# пример аннотирования и агрегации
# count_articles = User.objects.annotate(Count('article',distinct=True))
# print(count_articles)
# for user in count_articles:
#     print(user, user.article__count)

# пример аннотирования и агрегации:
#     max_article_count_user = User.objects.annotate(Count('article', distinct=True)).order_by('-article__count').first()
#     print(max_article_count_user)
#     max_article_count =  User.objects.annotate(Count('article', distinct=True)).aggregate(Max('article__count'))
#     max_article_count_user2 = User.objects.annotate(Count('article', distinct=True)).filter(article__count__exact=max_article_count['article__count__max'])
#     print(max_article_count_user2)

    # if request.method == 'POST':
    #     print('Получили post-запрос')
    #     print(request.POST)
    #     title = request.POST.get('title')
    #     price = request.POST.get('price')
    #     quantity = request.POST.get('quantity')
    #     new_product = Product(title, float(price), int(quantity))
    #     print('Создан товар: ', new_product.title, 'Общая сумма: ', new_product.amount())
    # else:
    #     print('Получили get-запрос')
    #
    # water = Product('Добрый сок', 40, 2)
    # chocolate = Product('Шоколад', 30, 1)
    # news_part = ['О животных', 'Природные явления', 'Наука и космос', 'Знаменитые люди']
    # context = {
    #     'news_part': news_part,
    #     'water': water,
    #     'chocolate': chocolate,
    #     'colors': colors,
    # }
    return render(request, 'main/index.html', context)
# def new_single (request):
#     return render(request, 'main/new_single.html')
def about (request):
    return render(request, 'main/about.html')

def sidebar (request):
    return render(request, 'main/sidebar.html')

def test_page (request):
    return render(request, 'main/test_page.html')

def get_demo(request,a,operation,b):
    if operation == 'minus':
            result = int(a) - int (b)
    elif operation == 'plus':
            result = int(a) + int(b)
    elif operation == 'multiply':
            result = int(a) * int(b)
    elif operation == 'divide':
            result = int(a) / int(b)
    else:
            return HttpResponse('Неверная команда')
    return HttpResponse(f'Вы ввели: {a} и {b} <br> Результат: {operation}:{result}')

def custom_404(request,exception):

    return render(request, 'main/custom_404.html')

# def news (request):
#     return render(request, 'main/news.html')



def base (request):
    return render(request, 'main/base.html')


@csrf_exempt
def update_server(request):
    # header_signature = request.META.get('HTTP_X_HUB_SIGNATURE')
    # verify_signature(request.body,settings.GITHUB_WEBHOOK_KEY,header_signature)

    if request.method == "POST":
        local_dir = '/home/Naddy777/RTK'
        repo = git.Repo(local_dir)
        repo.remotes.origin.pull()
        return HttpResponse("PythonAnywhere server updated successfully")
    else:
        return HttpResponse("Вы попали не туда")


# @csrf_exempt
# def update_server(request):
#     return HttpResponse("Хук работает")