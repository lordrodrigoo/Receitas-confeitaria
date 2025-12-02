import pytest
from django.urls import reverse
from recipes.models import Recipe, Category, User
from rest_framework.test import APIClient

class TestRecipeListAPIv1:
    @pytest.mark.django_db
    def test_get_empty(self):
        client = APIClient()
        response = client.get(reverse('recipes:recipes_public_api_v1'))
        assert response.status_code == 200
        assert response.data['results'] == []

    @pytest.mark.django_db
    def test_get_with_recipes(self):
        user = User.objects.create(username='user')
        category = Category.objects.create(name='Bolos')
        Recipe.objects.create(
            title='Bolo',
            description='desc',
            author=user,
            category=category,
            preparation_time=10,
            preparation_time_unit='min',
            servings=2,
            servings_unit='porcao',
            preparation_steps='passos',
            slug='bolo',
        )
        client = APIClient()
        response = client.get(reverse('recipes:recipes_public_api_v1'))
        assert response.status_code == 200
        assert response.data['count'] == 1
        assert response.data['results'][0]['title'] == 'Bolo'

class TestCategoryPublicListAPIView:
    @pytest.mark.django_db
    def test_get_empty(self):
        client = APIClient()
        response = client.get(reverse('recipes:categories_public_api_v1'))
        assert response.status_code == 200
        assert response.data == []

    @pytest.mark.django_db
    def test_get_with_categories(self):
        Category.objects.create(name='Bolos')
        Category.objects.create(name='Doces')
        client = APIClient()
        response = client.get(reverse('recipes:categories_public_api_v1'))
        assert response.status_code == 200
        names = [cat['name'] for cat in response.data]
        assert 'Bolos' in names
        assert 'Doces' in names
