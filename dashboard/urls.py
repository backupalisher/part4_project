from django.contrib.auth import views
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('brands', brands, name='brands'),
    path('models', models, name='models'),
    path('partcodes', partcodes, name='partcodes'),
    path('details', details, name='details'),
]