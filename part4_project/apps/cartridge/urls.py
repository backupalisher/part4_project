from django.urls import path
from . import views

app_name = 'cartridge'
urlpatterns = [
    path('', views.index, name='index'),
    path('cartridges/<int:brand_id>', views.cartridges, name='cartridges'),
    path('<int:cartridge_id>', views.cartridge, name='cartridge'),
]
