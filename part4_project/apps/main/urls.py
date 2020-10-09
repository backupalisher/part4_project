from django.urls import path
from .views import *


urlpatterns = [
    path('search', search),
    path('', index_models),
    # path('', index)
]