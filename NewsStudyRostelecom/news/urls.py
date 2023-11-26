from django.urls import path
from . import views

urlpatterns = [
    path('', views.news, name='news_index'),
    path('new_single/', views.new_single, name='new_single'),
    path('<int:id>', views.detail, name='news_detail'),

]
