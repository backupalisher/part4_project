from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('', views.cabinet, name='cabinet')
]