from django.urls import path
from . import views
from .api import *

app_name = 'detail'
urlpatterns = [
    path('', views.detail_view, name='detail_view'),
    path('<int:detail_id>', views.index, name='index'),
    path('create/', DetailsCreateView.as_view()),
    path('all/', DetailsListView.as_view()),
    path('edit/<int:pk>', DetailsEditView.as_view()),
]
