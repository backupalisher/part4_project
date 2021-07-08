from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('brands', brands, name='brands'),
    path('models', models, name='models'),
    path('partcodes', partcodes, name='partcodes'),
    path('modules', modules, name='modules'),
    path('prices', prices, name='prices'),
]
