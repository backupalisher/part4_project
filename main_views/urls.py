from django.urls import path, re_path

from part4_project.apps.model.api import ModelsCreateView, ModelsListView, ModelsEditView
from .views import *
from .model_views import *


urlpatterns = [
    path('model/create/', ModelsCreateView.as_view()),
    path('model/all/', ModelsListView.as_view()),
    path('model/edit/<int:pk>', ModelsEditView.as_view()),
    re_path(r'(?P<path>.*)$', index),
    # path('search', search),
    # path('models', index, in_url='models'),
    # path('models/', index, in_url='models'),
    # path('market', index_market),
    # path('market/', index_market),
    # path('supplies', index_supplies),
    # path('supplies/', index_supplies),
    # path('about', index_about),
    # path('about/', index_about),
    # path('', index_models),
    # path('', index)
]


