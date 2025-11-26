from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views.site import (
    RecipeHomeView, RecipeDetail,
    RecipeListViewSearch,
    RecipeAboutView,
    RecipeListViewCategory,
    RecipeCategoriesListView,
)
from .views.api_private import RecipeAPIv1ViewSet, CategoryPainelAPIViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.routers import DefaultRouter
from .views.api_public import RecipeListAPIv1, CategoryPublicListAPIView

import debug_toolbar

app_name = 'recipes'

router = DefaultRouter()
router.register(r'painel/recipes', RecipeAPIv1ViewSet, basename='painel-recipes')
router.register(r'painel/categories', CategoryPainelAPIViewSet, basename='painel-categories')

urlpatterns = [
	path('', RecipeHomeView.as_view(), name='home'),
    path('about/', RecipeAboutView.as_view(), name='about'),

    # All categories view
    path('recipe/categories/', RecipeCategoriesListView.as_view(), name='recipe-categories'),
    # One category view
    path('recipes/category/<int:category_id>/', RecipeListViewCategory.as_view(), name='category'),
	
    path('recipes/search/', RecipeListViewSearch.as_view(), name='search'),

    path('recipe/<int:pk>/', RecipeDetail.as_view(), name='recipe'),


    # API
    path('recipes/api/v1/', RecipeListAPIv1.as_view(), name='recipes_public_api_v1'),
    path('categories/api/v1/', CategoryPublicListAPIView.as_view(), name='categories_public_api_v1'),


    # JWT Auth endpoints
    path('recipes/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('recipes/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('recipes/api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + router.urls


