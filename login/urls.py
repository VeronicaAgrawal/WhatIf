from django.contrib import admin
from django.urls import path
from login import views

urlpatterns = [
     # path('', views.dashboard, name='dashboard'),
     path('editaccount/', views.editaccount, name='editaccount')
]