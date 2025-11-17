from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views.site import RecipeHomeView,RecipeDetail, RecipeListViewSearch, RecipeAboutView

import debug_toolbar

app_name = 'recipes'

urlpatterns = [
	path('', RecipeHomeView.as_view(), name='home'),
    path('about/', RecipeAboutView.as_view(), name='about'),
	path('recipes/search/', RecipeListViewSearch.as_view(), name='search'),

	path('recipes/category/<int:category_id>/', RecipeListViewSearch.as_view(), name='category'),
         
    path('recipe/<int:pk>/', RecipeDetail.as_view(), name='recipe'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


