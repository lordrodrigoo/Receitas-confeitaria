from django.shortcuts import render
from django.views.generic import ListView, DetailView
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


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe_detail.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs