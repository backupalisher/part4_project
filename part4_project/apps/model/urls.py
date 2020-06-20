from django.urls import path
from . import views

app_name = 'model'
urlpatterns = [
    # path('', views.detail_view, name='detail_view'),
    path('<int:model_id>', views.index, name='index'),
]