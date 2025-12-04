from django.urls import path
from .views.dashboard import dashboard_view
from .views.auth import login_view, login_create, logout_view
from .views.profile import AddPersonView, EditPersonView, UserDeleteView
from .views.category import CategoryDeleteView, CategoryEditView
from .views.dashboard_recipe import DashboardRecipe, DashboardRecipeDelete
from .views.api import AuthorViewSet
from rest_framework.routers import SimpleRouter



app_name = 'dashboard'


urlpatterns = [
    path('login/', login_view, name='login'),
    path('login/create/', login_create, name='login_create'),
    path('login/logout/', logout_view, name='logout'),

    path('dashboard', dashboard_view, name='dashboard'),
    path('dashboard/recipe/new/', DashboardRecipe.as_view(), name='dashboard_recipe_new'),
    path('dashboard/recipe/delete/', DashboardRecipeDelete.as_view(), name='dashboard_recipe_delete'),
    path('dashboard/recipe/<int:id>/edit/', DashboardRecipe.as_view(), name='dashboard_recipe_edit'),

    path('dashboard/add-person/', AddPersonView.as_view(), name='add_person'),
    path('dashboard/edit-person/<int:pk>/', EditPersonView.as_view(), name='edit_person'),
    path('dashboard/user/delete/', UserDeleteView.as_view(), name='dashboard_user_delete'),

    path('dashboard/category/delete/', CategoryDeleteView.as_view(), name='dashboard_category_delete'),
    path('dashboard/category/edit/<int:pk>/', CategoryEditView.as_view(), name='edit_category'),
]

author_api_router = SimpleRouter()
author_api_router.register(
    'api',
    AuthorViewSet,
    basename='dashboard-api'
)

urlpatterns += author_api_router.urls
