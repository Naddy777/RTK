from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('calc/<int:a>/<slug:operation>/<int:b>',views.get_demo),
    path('new_single/', views.new_single, name='new_single'),
    path('about/', views.about, name='about'),
    path('sidebar/', views.sidebar),
    path('test_page/', views.test_page),
    path('news/', views.news, name='news'),
    path('base/', views.base),
    path('base2/', views.base2),
    path('profile/', views.profile),
]
