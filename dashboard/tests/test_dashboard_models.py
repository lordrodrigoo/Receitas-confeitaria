import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from recipes.models import Recipe, Category
from django.utils.text import slugify
from unittest import mock



class TestCategoryModel:
    @pytest.mark.django_db
    def test_category_str(self):
        cat = Category.objects.create(name='Bolos')
        assert str(cat) == 'Bolos'

    @pytest.mark.django_db
    def test_category_meta(self):
        assert Category._meta.verbose_name == 'Categoria'
        assert Category._meta.verbose_name_plural == 'Categorias'
        assert Category._meta.ordering == ['name']


class TestRecipeModel:
    @pytest.mark.django_db
    def test_recipe_str(self):
        cat = Category.objects.create(name='Doces')
        user = User.objects.create(username='user')
        recipe = Recipe.objects.create(
            title='Bolo',
            description='desc',
            slug='bolo',
            preparation_time=10,
            preparation_time_unit='min',
            servings=2,
            servings_unit='porcao',
            preparation_steps='passos',
            category=cat,
            author=user,
        )
        assert str(recipe) == 'Bolo'

    @pytest.mark.django_db
    def test_recipe_get_absolute_url(self):
        cat = Category.objects.create(name='Doces')
        user = User.objects.create(username='user')
        recipe = Recipe.objects.create(
            title='Bolo',
            description='desc',
            slug='bolo',
            preparation_time=10,
            preparation_time_unit='min',
            servings=2,
            servings_unit='porcao',
            preparation_steps='passos',
            category=cat,
            author=user,
        )
        url = recipe.get_absolute_url()
        assert str(recipe.id) in url

    @pytest.mark.django_db
    def test_recipe_clean_duplicate_title(self):
        cat = Category.objects.create(name='Doces')
        user = User.objects.create(username='user')
        Recipe.objects.create(
            title='Bolo',
            description='desc',
            slug='bolo',
            preparation_time=10,
            preparation_time_unit='min',
            servings=2,
            servings_unit='porcao',
            preparation_steps='passos',
            category=cat,
            author=user,
        )
        recipe2 = Recipe(
            title='Bolo',
            description='desc2',
            slug='bolo2',
            preparation_time=5,
            preparation_time_unit='min',
            servings=1,
            servings_unit='porcao',
            preparation_steps='passos',
            category=cat,
            author=user,
        )
        with pytest.raises(ValidationError) as exc:
            recipe2.clean()
        assert 'Já existe uma receita com esse título.' in str(exc.value)

    @pytest.mark.django_db
    def test_recipe_clean_no_duplicate_for_same_instance(self):
        cat = Category.objects.create(name='Doces')
        user = User.objects.create(username='user')
        recipe = Recipe.objects.create(
            title='Bolo',
            description='desc',
            slug='bolo',
            preparation_time=10,
            preparation_time_unit='min',
            servings=2,
            servings_unit='porcao',
            preparation_steps='passos',
            category=cat,
            author=user,
        )
        # Should not raise for itself
        recipe.clean()

    @pytest.mark.django_db
    def test_recipe_save_slug_autogenerates(self, monkeypatch):
        cat = Category.objects.create(name='Doces')
        user = User.objects.create(username='user')
        recipe = Recipe(
            title='Bolo',
            description='desc',
            preparation_time=10,
            preparation_time_unit='min',
            servings=2,
            servings_unit='porcao',
            preparation_steps='passos',
            category=cat,
            author=user,
        )
        # Remove slug to test auto-generation
        recipe.slug = ''
        monkeypatch.setattr('random.SystemRandom.choices', lambda *a, **k: list('abc12'))
        recipe.save()
        assert recipe.slug.startswith(slugify('Bolo-abc12'))

    @pytest.mark.django_db
    def test_recipe_resize_image_called(self, monkeypatch):
        cat = Category.objects.create(name='Doces')
        user = User.objects.create(username='user')
        recipe = Recipe(
            title='Bolo',
            description='desc',
            slug='bolo',
            preparation_time=10,
            preparation_time_unit='min',
            servings=2,
            servings_unit='porcao',
            preparation_steps='passos',
            category=cat,
            author=user,
            cover='fake.jpg',
        )
        monkeypatch.setattr(Recipe, 'resize_image', mock.Mock())
        recipe.save()
        assert Recipe.resize_image.called
