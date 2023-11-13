from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('calc/<int:a>/<slug:operation>/<int:b>',views.get_demo),
    path('contacts/', views.contacts, name='contacts'),
    path('about/', views.about, name='about'),
    path('sidebar/', views.sidebar),
    path('test_page/', views.test_page),
]
