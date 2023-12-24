from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('calc/<int:a>/<slug:operation>/<int:b>',views.get_demo),
    path('about/', views.about, name='about'),
    path('sidebar/', views.sidebar),
    path('test_page/', views.test_page),
    path('base/', views.base),
    path('custom_404/', views.custom_404),

]
