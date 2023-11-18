from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_index, name='news_index'),
    path('news/', views.news_news, name='news_news'),
    path('show/<int:id>', views.detail, name='news_detail'),

]
