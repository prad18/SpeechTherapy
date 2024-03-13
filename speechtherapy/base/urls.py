from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('letters/', views.letters, name='letters'),
    path('base/',views.base, name='base'),
    path('register/',views.register, name='register'),
]