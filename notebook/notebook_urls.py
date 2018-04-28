# author HerbLee

from notebook import views
from django.contrib import admin
from django.urls import path

admin.autodiscover()

urlpatterns = [

    path('createitem/', views.createitem),
    path('update/', views.updateStatus),
    path('delete/', views.delete),
    path('getmodel/', views.getModel),
    path('gettoday/', views.getToday)

]
