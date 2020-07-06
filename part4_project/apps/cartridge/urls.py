from django.urls import path
from . import views
from .api import *

app_name = 'cartridge'
urlpatterns = [
    path('', views.index, name='index'),
    path('cartridges/<int:brand_id>', views.cartridges, name='cartridges'),
    path('<int:cartridge_id>', views.cartridge, name='cartridge'),
    path('create/', CartridgeCreateView.as_view()),
    path('all/', CartridgeListView.as_view()),
    path('edit/<int:pk>', CartridgeEditView.as_view()),
]
