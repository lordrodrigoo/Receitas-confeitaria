import pytest
from django.contrib.auth.models import User
from recipes.models import Recipe, Category
from rest_framework.test import APIClient
from django.urls import reverse

class TestRecipeAPIv1ViewSet:
    @pytest.mark.django_db
    def test_permission_denied_for_non_staff(self):
        user = User.objects.create_user(username='normal', password='123')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('recipes:painel-recipes-list'))
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_permission_allowed_for_staff(self):
        user = User.objects.create_user(username='staff', password='123', is_staff=True)
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('recipes:painel-recipes-list'))
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_recipe_list_pagination(self):
        user = User.objects.create_superuser(username='admin', password='123')
        category = Category.objects.create(name='Bolos')
        for i in range(12):
            Recipe.objects.create(
                title=f'Receita {i}',
                description='desc',
                slug=f'receita-{i}',
                preparation_time=10,
                preparation_time_unit='min',
                servings=2,
                servings_unit='porcao',
                preparation_steps='passos',
                category=category,
                author=user,
            )
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('recipes:painel-recipes-list'))
        assert response.status_code == 200
        assert 'results' in response.data
        assert len(response.data['results']) <= 9  # Default page size

class TestCategoryPainelAPIViewSet:
    @pytest.mark.django_db
    def test_permission_denied_for_non_staff(self):
        user = User.objects.create_user(username='normal', password='123')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('recipes:painel-categories-list'))
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_permission_allowed_for_superuser(self):
        user = User.objects.create_superuser(username='admin', password='123')
        Category.objects.create(name='Bolos')
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse('recipes:painel-categories-list'))
        assert response.status_code == 200
        assert isinstance(response.data, list)
        assert response.data[0]['name'] == 'Bolos'
