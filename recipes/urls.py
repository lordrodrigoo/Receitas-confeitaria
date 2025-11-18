from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views.site import (
    RecipeHomeView, RecipeDetail,
    RecipeListViewSearch,
    RecipeAboutView,
    RecipeListViewCategory,
    CategoryListView,
)
from .views.api import RecipeListAPIv1

import debug_toolbar

app_name = 'recipes'

urlpatterns = [
	path('', RecipeHomeView.as_view(), name='home'),
    path('about/', RecipeAboutView.as_view(), name='about'),
    path('categories/', CategoryListView.as_view(), name='categories'),
	path('recipes/search/', RecipeListViewSearch.as_view(), name='search'),

    path('recipes/category/<int:category_id>/', RecipeListViewCategory.as_view(), name='category'),
         
    path('recipe/<int:pk>/', RecipeDetail.as_view(), name='recipe'),

    # API 
    path('api/recipes/', RecipeListAPIv1.as_view(), name='api_recipes'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


