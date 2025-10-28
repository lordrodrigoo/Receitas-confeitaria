from recipes.views.site import home
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', home, name='home'),
]
