import pytest
from django.urls import reverse
from recipes.models import Recipe, Category
from django.contrib.auth.models import User
from django.test import Client
from django.http import Http404

class TestRecipeHomeView:
    @pytest.mark.django_db
    def test_home_view_status_and_template(self):
        client = Client()
        response = client.get(reverse('recipes:home'))
        assert response.status_code == 200
        assert 'recipes/pages/home.html' in [t.name for t in response.templates]

    @pytest.mark.django_db
    def test_home_view_context_categories(self):
        cat = Category.objects.create(name='Bolos')
        client = Client()
        response = client.get(reverse('recipes:home'))
        assert 'categories' in response.context
        assert list(response.context['categories']) == list(Category.objects.all())

class TestRecipeDetailView:
    @pytest.mark.django_db
    def test_detail_view_status_and_template(self):
        cat = Category.objects.create(name='Bolos')
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
        client = Client()
        response = client.get(reverse('recipes:recipe', args=[recipe.id]))
        assert response.status_code == 200
        assert 'recipes/pages/recipe_detail.html' in [t.name for t in response.templates]
        assert response.context['is_detail_page'] is True
        assert 'categories' in response.context

class TestRecipeAboutView:
    @pytest.mark.django_db
    def test_about_view_status_and_template(self):
        client = Client()
        response = client.get(reverse('recipes:about'))
        assert response.status_code == 200
        assert 'recipes/pages/about.html' in [t.name for t in response.templates]
        assert 'categories' in response.context

class TestRecipeListViewSearch:
    @pytest.mark.django_db
    def test_search_view_no_query_raises_404(self):
        client = Client()
        response = client.get(reverse('recipes:search'))
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_search_view_with_query(self):
        cat = Category.objects.create(name='Bolos')
        user = User.objects.create(username='user')
        Recipe.objects.create(
            title='Bolo de Chocolate',
            description='desc',
            slug='bolo-choc',
            preparation_time=10,
            preparation_time_unit='min',
            servings=2,
            servings_unit='porcao',
            preparation_steps='passos',
            category=cat,
            author=user,
        )
        client = Client()
        response = client.get(reverse('recipes:search') + '?q=chocolate')
        assert response.status_code == 200
        assert 'recipes/pages/search.html' in [t.name for t in response.templates]
        assert 'search_term' in response.context
        assert 'pagination_range' in response.context

class TestRecipeCategoriesListView:
    @pytest.mark.django_db
    def test_categories_list_view(self):
        Category.objects.create(name='Bolos')
        client = Client()
        response = client.get(reverse('recipes:recipe-categories'))
        assert response.status_code == 200
        assert 'recipes/pages/categories.html' in [t.name for t in response.templates]
        assert 'categories' in response.context

class TestRecipeListViewCategory:
    @pytest.mark.django_db
    def test_category_view_with_recipes(self):
        cat = Category.objects.create(name='Bolos')
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
        client = Client()
        response = client.get(reverse('recipes:category', args=[cat.id]))
        assert response.status_code == 200
        assert 'recipes/pages/category.html' in [t.name for t in response.templates]
        assert 'categories' in response.context
        assert response.context['title'] == cat.name

    @pytest.mark.django_db
    def test_category_view_no_recipes_raises_404(self):
        cat = Category.objects.create(name='Bolos')
        client = Client()
        response = client.get(reverse('recipes:category', args=[cat.id]))
        assert response.status_code == 404
