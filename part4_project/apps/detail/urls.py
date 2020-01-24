from django.urls import path
from . import views

app_name = 'detail'
urlpatterns = [
    path('', views.detail_view, name='detail_view'),
    path('<int:detail_id>', views.index, name='index'),
]