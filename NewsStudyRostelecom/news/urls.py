from django.urls import path
from . import views

urlpatterns = [
    path('', views.news, name='news_index'),
    path('new_single/', views.new_single, name='new_single'),
    path('<int:pk>', views.ArticleDetailView.as_view(), name='news_detail2'),  # отображение новости через дженерик
    path('<int:id>', views.detail, name='news_detail'), # первое отображение новости
    path('update/<int:pk>', views.ArticleUpdateView.as_view(), name='news_update'),
    path('delete/<int:pk>', views.ArticleDeleteView.as_view(), name='news_delete'),
    path('create/', views.create_article, name='create_article')

]
