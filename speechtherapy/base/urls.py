from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name='home'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/',views.registerPage, name='register'),
    path('learn/', views.learn, name='learn'),
    path('letters/',views.letters,name='letters'),
]