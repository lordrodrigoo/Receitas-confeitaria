import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from recipes.models import Recipe
from .utils import get_tokens_for_user


@pytest.mark.django_db
def test_painel_list_requires_auth(admin_user):
    client = APIClient()
    url = reverse('recipes:painel-recipes-list')
    resp = client.get(url)
    assert resp.status_code == 401


@pytest.mark.django_db
def test_painel_list_forbidden_for_normal_user():
    User = get_user_model()
    normal = User.objects.create_user(username='normal', password='123')
    client = APIClient()
    client.force_authenticate(user=normal)
    url = reverse('recipes:painel-recipes-list')
    resp = client.get(url)
    assert resp.status_code == 403


@pytest.mark.django_db
def test_painel_list_and_create(admin_user):
    client = APIClient()
    tokens = get_tokens_for_user(admin_user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

    url = reverse('recipes:painel-recipes-list')
    resp = client.get(url)
    assert resp.status_code == 200

    payload = {
        'title': 'API Test Cake',
        'description': 'desc',
        'preparation_time': 10,
        'preparation_time_unit': 'min',
        'servings': 2,
        'servings_unit': 'porcao',
        'preparation_steps': 'mix and bake',
        'author': admin_user.id,
    }

    resp = client.post(url, payload, format='json')
    assert resp.status_code == 201, resp.data

    assert Recipe.objects.filter(title='API Test Cake').exists()
