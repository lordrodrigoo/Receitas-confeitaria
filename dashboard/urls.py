from django.urls import path
from . import views
from .views.category_delete import CategoryDeleteView
from .views.user_delete import UserDeleteView
from rest_framework.routers import SimpleRouter



app_name = 'dashboard'

author_api_router = SimpleRouter()
author_api_router.register(
    'api',
    views.AuthorViewSet,
    basename='dashboard-api'
)


urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('login/logout/', views.logout_view, name='logout'),

    path('dashboard', views.dashboard, name='dashboard' ),
    path('dashboard/recipe/new/', views.DashboardRecipe.as_view(), name='dashboard_recipe_new' ),
    path('dashboard/recipe/delete/', views.DashboardRecipeDelete.as_view(), name='dashboard_recipe_delete' ),
    path('dashboard/recipe/<int:id>/edit/', views.DashboardRecipe.as_view(), name='dashboard_recipe_edit' ),

    path('dashboard/add-person/', views.add_person, name='add_person'),

    path('dashboard/category/delete/', CategoryDeleteView.as_view(), name='dashboard_category_delete'),
    path('dashboard/user/delete/', UserDeleteView.as_view(), name='dashboard_user_delete'),

]

urlpatterns += author_api_router.urls
