from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from .models import *
from django.http import HttpResponse, JsonResponse
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db import connection, reset_queries
from django.views.generic import DetailView, DeleteView, UpdateView
from django.conf import settings
import json
from django.contrib import messages
from django.core.paginator import Paginator
from .utils import ViewCountMixin
from users.utils import check_group #импортировли декоратор
from django.conf import settings
from django.db.models import Q

#Для поиска в шаблоне списка новостей
def search_auto(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        q = request.GET.get('term','')
        articles = Article.objects.filter(title__icontains=q)
        results =[]
        for a in articles:
            results.append(a.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data,mimetype)

#Для поиска в сайдбаре
def search_auto1(request):
    print('2вызов функции')
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        q = request.GET.get('term','')
        articles = Article.objects.filter(title__icontains=q)
        results =[]
        for a in articles:
            results.append(a.title)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    print('2Работает?', results)
    return HttpResponse(data,mimetype)

def search(request):
    if request.method == 'POST': #пришел запрос из бокового меню
        value = request.POST['search_input'] #находим новости
        articles = Article.objects.filter(title__icontains=value)
        if len(articles) == 1: #если одна- сразу открываем подробное отображение новости
            return render(request, 'news/new_single.html', {'article': articles[0]})
        else:
            #если несколько - отправляем человека в функцию index со страницей-списком новостей и фильтрами
            #не забываем передать поисковый запрос:
            # либо через сессии:
            request.session['search_input'] = value
            return redirect('news')
            #либо через фрагмент URLссылки:
            # но в таком случае придётся обрабатывать ссылку в Urls
            #функция reverse из модуля Urls добавит переданные аргументы в качестве get-аргументов.
            # return redirect(reverse('news', kwargs={'search_input':value}))

            # return render(request, 'news/news_list.html', {'articles': articles})
    else:
        return redirect('home')

def news(request):
    user_list = User.objects.all() #Список всех юзеров#
    category_list = Article.categories
    if request.method == "POST":
        selected_a = int(request.POST.get('author_filter'))
        selected_c = int(request.POST.get('category_filter'))
        request.session['selected_a'] = selected_a
        request.session['selected_c'] = selected_c
        if selected_a == 0:
            articles = Article.objects.all().order_by('-date')
        else:
            articles = Article.objects.filter(author=selected_a).order_by('-date')
        if selected_c != 0:
            articles = articles.filter(category__icontains=category_list[selected_c - 1][0]).order_by('-date')
    else:
        selected_a = request.session.get('selected_a')
        if selected_a != None: #если не пустое - находим нужные ноновсти
            articles = Article.objects.filter(author=selected_a).order_by('-date')
        else:
            selected_a = 0
        selected_c = 0
        value = request.session.get('search_input')  # вытаскиваем из сессии значение поиска
        if value != None:  # если не пустое - находим нужные ноновсти
            articles = Article.objects.filter(title__icontains=value).order_by('-date')
            del request.session['search_input']  # чистим сессию, чтобы этот фильтр не "заело"
        else:
            # если не оказалось таокго ключика или запрос был кривой - отображаем все элементы
            articles = Article.objects.all().order_by('-date')
    # articles = Article.objects.all().order_by('-date')
    total = len(articles)
    p = Paginator(articles,3)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {'articles': page_obj, 'author_list': user_list,  'selected_a': selected_a, 'categories': category_list, 'selected_c': selected_c, 'total':total}
    return render(request, 'news/news.html', context)


# def search1(request):
#     if request.method == 'POST': #пришел запрос из бокового меню
#         value = request.POST['search_input1'] #находим новости
#         articles = Article.objects.filter(title__contains=value)
#         if len(articles) == 1: #если одна- сразу открываем подробное отображение новости
#             return render(request, 'news/new_single.html', {'article': articles[0]})
#         else:
#             #если несколько - отправляем человека в функцию index со страницей-списком новостей и фильтрами
#             #не забываем передать поисковый запрос:
#             # либо через сессии:
#             request.session['search_input1'] = value
#             return redirect('news22')
#             #либо через фрагмент URLссылки:
#             # но в таком случае придётся обрабатывать ссылку в Urls
#             #функция reverse из модуля Urls добавит переданные аргументы в качестве get-аргументов.
#             # return redirect(reverse('news', kwargs={'search_input':value}))
#
#             # return render(request, 'news/news_list.html', {'articles': articles})
#     else:
#         return redirect('home')


# def news22(request):
#     user_list = User.objects.all() #Список всех юзеров#
#     category_list = Article.categories
#     if request.method == "POST":
#         selected_a = int(request.POST.get('author_filter'))
#         selected_c = int(request.POST.get('category_filter'))
#         request.session['selected_a'] = selected_a
#         request.session['selected_c'] = selected_c
#         if selected_a == 0:
#             articles = Article.objects.all().order_by('-date')
#         else:
#             articles = Article.objects.filter(author=selected_a).order_by('-date')
#         if selected_c != 0:
#             articles = articles.filter(category__icontains=category_list[selected_c - 1][0])
#     else:
#         selected_a = request.session.get('selected_a')
#         if selected_a != None: #если не пустое - находим нужные ноновсти
#             articles = Article.objects.filter(author=selected_a)
#         else:
#             selected_a = 0
#         selected_c = 0
#         articles = Article.objects.all().order_by('-date')
#     total = len(articles)
#     p = Paginator(articles,3)
#     page_number = request.GET.get('page')
#     page_obj = p.get_page(page_number)
#     context = {'articles': page_obj, 'author_list': user_list,  'selected_a': selected_a, 'categories': category_list, 'selected_c': selected_c, 'total':total}
#     return render(request, 'news/news.html', context)



class ArticleDetailView(ViewCountMixin, DetailView):
    model = Article
    template_name = 'news/new_single.html'
    context_object_name = 'article'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_object = self.object
        images = Image.objects.filter(article=current_object)
        context['images'] = images
        return context

class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'news/create_article.html'
    fields = ['title','anouncement','text', 'tags','category']



# def password_update(request):
#     user = request.user
#     form = PasswordChangeForm(user,request.POST)
#     if request.method == 'POST':
#         if form.is_valid():
#             password_info = form.save()
#             update_session_auth_hash(request,password_info)
#             messages.success(request,'Пароль успешно изменен')
#             return redirect('profile')
#
#     context = {"form": form}
#     return render(request,'users/edit_password.html',context)

class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('news_index')
    template_name = 'news/delete_news.html'


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

def news2(request):
    user_list = User.objects.all() #Список всех юзеров#
    category_list = Article.categories
    if request.method == "POST":
        selected_a = int(request.POST.get('author_filter'))
        selected_c = int(request.POST.get('category_filter'))
        request.session['selected_a'] = selected_a
        request.session['selected_c'] = selected_c
        if selected_a == 0:
            articles = Article.objects.all().order_by('-date')
        else:
            articles = Article.objects.filter(author=selected_a).order_by('-date')
        if selected_c != 0:
            articles = articles.filter(category__icontains=category_list[selected_c - 1][0])
    else:
        selected_a = request.session.get('selected_a')
        if selected_a != None:  # если не пустое - находим нужные ноновсти
            articles = Article.objects.filter(author=selected_a)
        else:
            selected_a = 0
        selected_c = 0
        value = request.session.get('search_input')  # вытаскиваем из сессии значение поиска
        if value != None:  # если не пустое - находим нужные ноновсти
            articles = Article.objects.filter(title__icontains=value)
            del request.session['search_input']  # чистим сессию, чтобы этот фильтр не "заело"
        else:
            # если не оказалось таокго ключика или запрос был кривой - отображаем все элементы
            articles = Article.objects.all().order_by('-date')
        # articles = Article.objects.all().order_by('-date')
    context = {'articles': articles, 'author_list': user_list,  'selected_a': selected_a, 'categories': category_list, 'selected_c': selected_c}
    return render(request, 'news/news2.html', context)

# def index(request):
#     #пример применения пользовательского менджера
#     articles = Article.published.all()
#     context={'today_articles': articles} #Это пример
#     author_list = User.objects.all()
#     selected = 0
#     if request.method=="POST":
#         # print(request.POST)
#         selected = int(request.POST.get('author_filter'))
#         if selected == 0:
#             articles = Article.objects.all()
#         else:
#             articles = Article.objects.filter(author=selected)
#         # print(connection.queries)
#     else:
#         articles = Article.objects.all()
#         p = Paginator(articles,2)
#     page_number = request.GET.get('page')
#     page_obj = p.get_page(page_number)
#     print(page_obj)
#     context = {'articles': page_obj, 'author_list': author_list, 'selected': selected}
#
#     return render(request,'news/news.html',context)


def new_single (request):
    article = Article.objects.all().last()
    context = {'article': article}
    return render(request, 'news/new_single.html', context)

def new_single2 (request):
    article = Article.objects.all().last()
    context = {'article': article}
    return render(request, 'news/new_single2.html', context)

# def index(request):
#     article = Article.objects.all().first()
#     context = {'article':article}
#     return render(request,'news/index.html',context)

def detail(request, id):
    article = Article.objects.filter(id=id).first()
    context = {'article': article}
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

@login_required (login_url=settings.LOGIN_URL) #человек не аутентифицирован - отправляем на другую страницу
@check_group('Author')  #пример использования декоратора
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            if current_user.id !=None: #проверили что не аноним
                new_article = form.save(commit=False) #появится экземпляр новой статьи, но не будет сохранен в БД
                new_article.author = current_user
                new_article.save() #сохраняем в БД
                form.save_m2m() # добавляем связи много ко многим
                # form = ArticleForm() # обнуляем (чистим) форму
                for img in request.FILES.getlist('image_field'):
                    Image.objects.create(article=new_article, image=img, title=img.name)
                return redirect('news_index')
    else:
        form = ArticleForm()
    return render(request,'news/create_article.html', {'form':form})

def article_update(request,id):
    article = Article.objects.filter(id=id).first()
    if request.method == "POST":
        article_form = ArticleUpdateForm(request.POST, request.FILES, instance=article)
        if article_form.is_valid():
            user = request.user
            if user.id !=None: #проверили что не аноним
                article = article_form.save(commit=False)
                article.author = user
                article.save()
                article_form.save_m2m()
                for img in request.FILES.getlist('image_field'):
                    Image.objects.create(article=article, image=img, title=img.name)
                messages.success(request, "Статья успешно обновлена")
                return redirect('new_single')
    else:
        article_form = ArticleUpdateForm(instance=article)
    context = { 'article_form':article_form}
    return render(request,'news/edit_news.html', context)

def detail2(request, id):
    article = Article.objects.filter(id=id).first()
    context = {'article': article}
    return render(request, 'news/new_single.html', context)





