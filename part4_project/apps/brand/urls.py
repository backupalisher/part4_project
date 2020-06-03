from django.urls import path
from . import views

app_name = 'brand'
urlpatterns = [
    path('', views.index, name='index'),
    path('brands/', views.brands, name='brands'),
    path('<int:brand_id>', views.index, name='index'),
]
