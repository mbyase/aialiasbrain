# coding=utf-8
# author HerbLee

from account import views
from django.contrib import admin
from django.urls import path

admin.autodiscover()

urlpatterns = [

    # index视图
    path('register/', views.register),
    path('check/', views.check_account),
    path('login/', views.login),
    path('get/', views.get_account),
]