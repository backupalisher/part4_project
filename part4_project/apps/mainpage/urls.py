from django.urls import path
from part4_project.apps.mainpage import views


urlpatterns = [
    path('', views.index, name='index')
]