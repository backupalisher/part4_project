from django.urls import path
from . import views
from .api import *

app_name = 'model'
urlpatterns = [
    # path('', views.detail_view, name='detail_view'),
    path('<int:model_id>', views.index, name='index'),
    path('create/', ModelsCreateView.as_view()),
    path('all/', ModelsListView.as_view()),
    path('edit/<int:pk>', ModelsEditView.as_view()),
]