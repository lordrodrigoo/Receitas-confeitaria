from django.shortcuts import render
from django.views.generic import ListView
from recipes.models import Recipe


# Create your views here.

app_name = 'recipes'



class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipes/pages/home.html'
    ordering = ['-id']



class RecipeHomeView(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

