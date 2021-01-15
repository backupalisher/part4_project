from django.urls import path
from .views import *


urlpatterns = [
    path('search', search),
    path('market', index_models),
    path('market/', index_models),
    path('', index_models),
    # path('', index)
]