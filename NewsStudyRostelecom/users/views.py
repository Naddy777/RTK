from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import AccountUpdateForm, UserUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from news.models import Article
from django.core.paginator import Paginator


def delete_profile(request):
    return render(request, 'users/delete_profile.html')

@login_required
def del_user(request):
    user = request.user
    user.delete()
    # Account.objects.delete(user=user)
    return redirect ('login')

@login_required
def add_to_favorites(request, id):
    article = Article.objects.get(id=id)
    #проверям есть ли такая закладка с этой новостью
    bookmark = FavoriteArticle.objects.filter(user=request.user.id,
                                              article=article)
    if bookmark.exists():
        bookmark.delete()
        messages.warning(request,f"Новость {article.title} удалена из закладок")
    else:
        bookmark = FavoriteArticle.objects.create(user=request.user, article=article)
        messages.success(request,f"Новость {article.title} добавлена в закладки")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def favorites_articles(request):
    # article = Article.objects.all()
    bookmark = FavoriteArticle.objects.filter(user=request.user).order_by('-create_at')
    total = len(bookmark)
    p = Paginator(bookmark,3)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {'articles': page_obj, 'total':total,}
    return render(request, 'users/favorites_articles.html', context)




def profile(request):
    context = dict()
    return render(request,'users/profile.html',context)

def profile_update(request):
    user = request.user
    account = Account.objects.get(user=user)
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=user)
        account_form = AccountUpdateForm(request.POST, request.FILES, instance=account)
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            messages.success(request,"Профиль успешно обновлен")
            return redirect('profile')
    else:
        context = {'account_form':AccountUpdateForm(instance=account),
                   'user_form':UserUpdateForm(instance=user)}
    return render(request,'users/edit_profile.html', context)



def password_update(request):
    user = request.user
    form = PasswordChangeForm(user,request.POST)
    if request.method == 'POST':
        if form.is_valid():
            password_info = form.save()
            update_session_auth_hash(request,password_info)
            messages.success(request,'Пароль успешно изменен')
            return redirect('profile')

    context = {"form": form}
    return render(request,'users/edit_password.html',context)


def registration(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            category = request.POST['account_type']
            if category == 'author':
                group = Group.objects.get(name='Actions_Required')
                user.groups.add(group)
            else:
                group = Group.objects.get(name='Reader')
                user.groups.add(group)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            account = Account.objects.create(user=user, nickname=user.username)
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'{username} был зарегистрирован!')
            return redirect('home')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request,'users/registration.html', context)


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
    return render(request,'users/contact_page.html')

def user_panel (request):
    return render(request, 'users/user_panel.html')


def my_articles(request):
    category_list = Article.categories #создали перечень категорий
    author = User.objects.get(id=request.user.id)
    articles = Article.objects.filter(author=author).order_by('-date')
    if request.method == "POST":
        selected_c = int(request.POST.get('category_filter'))
        if selected_c != 0: #фильтруем найденные результаты по категориям
            articles = articles.filter(category__icontains=category_list[selected_c - 1][0])
    else: #если страница открывется впервые
        selected_c = 0
    total = len(articles)
    p = Paginator(articles,4)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    context = {'articles': page_obj, 'total':total,
               'categories':category_list,'selected_c': selected_c}

    return render(request,'users/my_articles.html',context)

