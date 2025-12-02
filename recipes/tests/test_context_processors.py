import pytest
from django.test import RequestFactory
from recipes.context_processors import categories
from recipes.models import Category

@pytest.mark.django_db
def test_categories_returns_all_categories():
    Category.objects.create(name='Bolos')
    Category.objects.create(name='Doces')
    request = RequestFactory().get('/')
    context = categories(request)
    assert 'categories' in context
    assert list(context['categories'].values_list('name', flat=True)) == ['Bolos', 'Doces']

@pytest.mark.django_db
def test_categories_empty():
    request = RequestFactory().get('/')
    context = categories(request)
    assert 'categories' in context
    assert list(context['categories']) == []
