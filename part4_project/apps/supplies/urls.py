from django.urls import path
from . import views
from .api import *

app_name = 'supplies'
urlpatterns = [
    path('', views.index, name='index'),
    path('supplies/<int:brand_id>', views.supplies, name='supplies'),
    path('<int:supplie_id>', views.supplie, name='supplies'),
    path('create/', SupplieCreateView.as_view()),
    path('all/', SupplieListView.as_view()),
    path('edit/<int:pk>', SupplieEditView.as_view()),
]
