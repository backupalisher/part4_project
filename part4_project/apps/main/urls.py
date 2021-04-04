from django.urls import path
from part4_project.apps.main.views import *


urlpatterns = [
    path('search', search),
    path('market', index_models),
    path('market/', index_models),
    path('market/', index_models),
    path('', index_models),
    # path('', index)
]