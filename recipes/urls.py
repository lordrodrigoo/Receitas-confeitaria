
from django.urls import path
from .views.site import RecipeHomeView

app_name = 'recipes'

urlpatterns = [
	path('', RecipeHomeView.as_view(), name='home'),
]
