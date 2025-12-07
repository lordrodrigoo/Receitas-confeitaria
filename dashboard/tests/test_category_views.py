import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from dashboard.tests.test_dashboard_base import DashboardTestBase
from recipes.models import Category, Recipe

class TestCategoryViews(DashboardTestBase):
    def setUp(self):
        super().setUp()
        self.superuser = self.make_user(username='admin', is_superuser=True)
        self.login(self.superuser)
        self.category = self.make_category(name='Doces')

    def test_delete_category_with_recipes(self):
        recipe = self.make_recipe(category=self.category)
        url = reverse('dashboard:dashboard_category_delete')
        response = self.client.post(url, {'category_id': self.category.id}, follow=True)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        assert any('Não é possível excluir uma categoria que possui receitas.' in m for m in messages)
        assert Category.objects.filter(id=self.category.id).exists()

    def test_delete_category_without_recipes(self):
        url = reverse('dashboard:dashboard_category_delete')
        response = self.client.post(url, {'category_id': self.category.id}, follow=True)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        assert any('Categoria excluída com sucesso!' in m for m in messages)
        assert not Category.objects.filter(id=self.category.id).exists()

    def test_delete_category_invalid_form(self):
        url = reverse('dashboard:dashboard_category_delete')
        response = self.client.post(url, {'invalid_field': 123}, follow=True)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        assert any('Requisição inválida para exclusão de categoria.' in m for m in messages)

    def test_delete_category_not_found(self):
        from django.urls import reverse
        from django.contrib.messages import get_messages
        url = reverse('dashboard:dashboard_category_delete')
        # Usa um ID que não existe
        response = self.client.post(url, {'category_id': 99999}, follow=True)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        assert any('Requisição inválida para exclusão de categoria.' in m for m in messages)

    def test_edit_category_get(self):
        from unittest.mock import patch
        from django.http import HttpResponse
        url = reverse('dashboard:edit_category', args=[self.category.id])
        with patch('dashboard.views.category.render') as mock_render:
            mock_render.return_value = HttpResponse('ok', status=200)
            response = self.client.get(url)
            assert response.status_code == 200

    def test_edit_category_post_valid(self):
        url = reverse('dashboard:edit_category', args=[self.category.id])
        response = self.client.post(url, {'name': 'Salgados'}, follow=True)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        assert any('Categoria editada com sucesso!' in m for m in messages)
        self.category.refresh_from_db()
        assert self.category.name == 'Salgados'

    def test_edit_category_post_invalid(self):
        url = reverse('dashboard:edit_category', args=[self.category.id])
        response = self.client.post(url, {'name': ''})
        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors
