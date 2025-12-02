import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from recipes.models import Category, Recipe
from dashboard.views import category_delete
from dashboard.forms.category_delete_form import CategoryDeleteForm



class TestCategoryDeleteView:
    @pytest.mark.django_db
    def test_delete_category_requires_superuser(self):
        user = User.objects.create_user(username='normal', password='123')
        client = Client()
        client.login(username='normal', password='123')
        category = Category.objects.create(name='Teste')
        form = CategoryDeleteForm({'category_id': category.id})
        response = client.post(reverse('dashboard:dashboard_category_delete'), data=form.data)
        # Redirect, is not superuser
        assert response.status_code == 302
        expected_url = reverse('dashboard:dashboard') + '?next=' + reverse('dashboard:dashboard_category_delete')
        assert response.url == expected_url

    @pytest.mark.django_db
    def test_delete_category_with_recipes(self):
        user = User.objects.create_superuser(username='admin', password='123')
        client = Client()
        client.login(username='admin', password='123')
        category = Category.objects.create(name='Teste')
        Recipe.objects.create(
            title='Bolo',
            description='desc',
            slug='bolo',
            preparation_time=10,
            preparation_time_unit='min',
            servings=2,
            servings_unit='porcao',
            preparation_steps='passos',
            category=category,
            author=user,
        )
        form = CategoryDeleteForm({'category_id': category.id})
        response = client.post(reverse('dashboard:dashboard_category_delete'), data=form.data, follow=True)
        assert Category.objects.filter(id=category.id).exists()
        assert 'Não é possível excluir uma categoria que possui receitas.' in response.content.decode()

    @pytest.mark.django_db
    def test_delete_category_success(self):
        user = User.objects.create_superuser(username='admin', password='123')
        client = Client()
        client.login(username='admin', password='123')
        category = Category.objects.create(name='Teste')
        form = CategoryDeleteForm({'category_id': category.id})
        response = client.post(reverse('dashboard:dashboard_category_delete'), data=form.data, follow=True)
        assert not Category.objects.filter(id=category.id).exists()
        assert 'Categoria excluída com sucesso!' in response.content.decode()

    @pytest.mark.django_db
    def test_delete_category_invalid_form(self):
        user = User.objects.create_superuser(username='admin', password='123')
        client = Client()
        client.login(username='admin', password='123')
        form = CategoryDeleteForm({'category_id': ''})
        response = client.post(reverse('dashboard:dashboard_category_delete'), data=form.data, follow=True)
        assert 'Requisição inválida para exclusão de categoria.' in response.content.decode()
