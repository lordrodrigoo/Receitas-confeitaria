from django.test import TestCase
from recipes.models import Recipe

class RecipeMixin:
    def make_recipe(
            self,
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='minutes',
            servings=2,
            servings_unit='people',
            preparation_steps='Recipe Preparation Steps',
            preparation_steps_is_html=False,
            cover='',
    ):
        recipe = Recipe.objects.create(
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            cover=cover,
        )
        return recipe
    
class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self):
        return super().setUp()