
from django.test import TestCase
from recipes.models import Category, Recipe, User


class RecipeMixin:
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(self, username='username', password='123456'):
        return User.objects.create_user(username=username, password=password)

    def make_recipe(
        self,
        title='Recipe Title',
        description='Recipe Description',
        slug='recipe-slug',
        preparation_time=10,
        preparation_time_unit='min',
        servings=5,
        servings_unit='porcao',
        preparation_steps='Recipe Preparation Steps',
        preparation_steps_is_html=False,
        cover='',
        category=None,
        author=None,
    ):
        if category is None:
            category = self.make_category()
        if author is None:
            author = self.make_author()
        return Recipe.objects.create(
            category=category,
            author=author,
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

    def make_recipe_in_batch(self, qtd=10):
        recipes = []
        for i in range(qtd):
            recipe = self.make_recipe(
                title=f'Recipe Title {i}',
                slug=f'r{i}',
                author=self.make_author(username=f'u{i}')
            )
            recipes.append(recipe)
        return recipes

class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
    