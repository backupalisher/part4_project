# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views
from main_views.decorators import check_recaptcha

# from django.urls import path


urlpatterns = [
    url(r'^login/$', check_recaptcha(views.login), name='login'),
    url(r'^register/$', check_recaptcha(views.register), name='register'),
    url(r'^cabinet/$', views.cabinet, name='cabinet'),
    url(r'^logout/$', views.logout_view, name='cabinet'),
    url('', views.cabinet, name='cabinet'),

    # path('logout/', views.logout, name='logout'),
    #
    # path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #
    # path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]