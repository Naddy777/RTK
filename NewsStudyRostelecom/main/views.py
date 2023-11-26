from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import News, Product
from news.models import Article
from django.db.models import Count, Avg
from django.contrib.auth.models import User
def index (request):
#     value = -10
#     n1 = News('Новость 1', 'Текст 1', '07.11.23')
#     n2 = News('Новость 2', 'Текст 1', '07.11.23')
#     l = [n1, n2]
#     m = ['раз', 'два', 'три']
#     context = {'title': 'Мой сайт',
#             'Header1': 'Заголовок страницы',
#                'value': value,
#                'numbers': l,
#                'numbers2': m,
#                }
    colors = ['red', 'blue', 'golden', 'black']
#    context1 = {
#      'colors': colors
#     }
# Примеры values, values_list:
#     all_news = Article.objects.all().values('author','title')
#     for a in all_news:
#         print(a['author'], a['title'])
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

    if request.method == 'POST':
        print('Получили post-запрос')
        print(request.POST)
        title = request.POST.get('title')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        new_product = Product(title, float(price), int(quantity))
        print('Создан товар: ', new_product.title, 'Общая сумма: ', new_product.amount())
    else:
        print('Получили get-запрос')

    water = Product('Добрый сок', 40, 2)
    chocolate = Product('Шоколад', 30, 1)
    news_part = ['О животных', 'Природные явления', 'Наука и космос', 'Знаменитые люди']
    context = {
        'news_part': news_part,
        'water': water,
        'chocolate': chocolate,
        'colors': colors,
    }
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
    return HttpResponse(f'Страница не найдена. Код ошибки:  {exception}')

# def news (request):
#     return render(request, 'main/news.html')

def profile (request):
    return render(request, 'main/profile.html')

def base (request):
    return render(request, 'main/base.html')
