import pytest
from recipes.models import Recipe
from .test_recipe_base import RecipeTestBase, Recipe


class RecipeModelRecipeTest(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def make_recipe_no_default(self):
        import uuid
        unique_id = uuid.uuid4().hex[:8] # Generate a unique ID

        recipe = Recipe(
            title='Unique Recipe Title',
            description='Unique Recipe Description',
            slug=f'unique-recipe-slug-{unique_id}',
            preparation_time=15,
            preparation_time_unit='minutes',
            servings=4,
            servings_unit='people',
            preparation_steps='Unique Recipe Preparation Steps',
            preparation_steps_is_html=False,
            is_published=False,
            cover='',
        )
        recipe.full_clean()  # This will validate the model fields
        recipe.save()
        return recipe

    def test_recipe_creation(self):
        recipe = self.make_recipe_no_default()
        self.assertIsInstance(recipe, Recipe)
        self.assertEqual(recipe.title, 'Unique Recipe Title')
        self.assertEqual(recipe.description, 'Unique Recipe Description')
        self.assertTrue(recipe.slug.startswith('unique-recipe-slug-'))
        self.assertEqual(recipe.preparation_time, 15)
        self.assertEqual(recipe.preparation_time_unit, 'minutes')
        self.assertEqual(recipe.servings, 4)
        self.assertEqual(recipe.servings_unit, 'people')
        self.assertEqual(recipe.preparation_steps, 'Unique Recipe Preparation Steps')
        self.assertFalse(recipe.preparation_steps_is_html)
        self.assertFalse(recipe.is_published)
        self.assertEqual(recipe.cover, '')