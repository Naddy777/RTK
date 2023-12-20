from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='user_index'),
    path('contact_page',views.contact_page,name='contact_page'),
    path('registration', views.registration, name='registration'),
    path('login', auth_views.LoginView.as_view(
        template_name='users/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(
        template_name='users/logout.html'), name='logout'),
    path('user_panel',views.user_panel,name='user_panel'),
    path('profile', views.profile, name='profile'),
    path('profile/update', views.profile_update, name='profile_update'),
    path('password', views.password_update, name='password'),
    path('myarticles',views.my_articles,name='my_articles'),
    path('favorites/<int:id>', views.add_to_favorites, name='favorites'),
    path('favarticles', views.favorites_articles, name='favorites_articles'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('delete_confirm/', views.del_user, name='delete_confirm'),
  ]
