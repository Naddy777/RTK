from django.urls import path
from . import views

urlpatterns = [
    path('', views.news, name='news_index'),
    path('news2/', views.news2),
    path('new_single/', views.new_single, name='new_single'),
    path('<int:pk>', views.ArticleDetailView.as_view(), name='news_detail2'),  # отображение новости через дженерик
    path('<int:id>', views.detail, name='news_detail'), # первое отображение новости
    path('update/<int:pk>', views.ArticleUpdateView.as_view(), name='news_update'),
    path('edit/<int:id>', views.article_update, name='edit_news'),
    path('delete/<int:pk>', views.ArticleDeleteView.as_view(), name='news_delete'),
    path('search_auto1/', views.search_auto1, name='search_auto11'),
    path('search_auto/', views.search_auto, name='search_auto'),
    path('create/', views.create_article, name='create_article')

]
