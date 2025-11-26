from django.urls import path 
from . import views
from django.urls import include


app_name = 'authors'

urlpatterns = [
    path('profile/<int:id>/', views.ProfileView.as_view(), name='public-profile'),
    
]

