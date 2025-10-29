import pytest
from django.urls import reverse, resolve
from .test_recipe_base import RecipeTestBase
from recipes.views.site import RecipeHomeView
from recipes.models import Recipe



class RecipeHomeViewTest(RecipeTestBase):
        def test_recipe_home_view_function_is_correct(self):
                view = resolve(reverse('recipes:home'))
                self.assertIs(view.func.view_class, RecipeHomeView)


        def test_recipe_home_view_returns_status_code_200_OK(self):
                response = self.client.get(reverse('recipes:home'))
                assert response.status_code == 200


        def test_recipe_home_view_loads_correct_template(self):
                response = self.client.get(reverse('recipes:home'))
                self.assertTemplateUsed(response, 'recipes/pages/home.html')

        def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
                Recipe.objects.all().delete() 
                response = self.client.get(reverse('recipes:home'))
                self.assertContains(response, 'Não encontramos receitas aqui! 😢')