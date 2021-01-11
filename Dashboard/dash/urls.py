from django.urls import path

from . import views

urlpatterns = [
    path('home', views.home, name = 'graph'),
    path('', views.home, name ='home')


]