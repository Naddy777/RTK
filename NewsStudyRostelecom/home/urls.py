from django.urls import path

from .import views
urlpatterns = [
    path('', views.index, name='demo'),
    path('demo_form/', views.demo_form),
    path('showlastmodel/', views.showlastmodel),


]
