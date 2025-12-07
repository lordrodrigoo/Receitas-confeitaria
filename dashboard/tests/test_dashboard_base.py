import pytest
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from recipes.models import Recipe, Category

User = get_user_model()

class DashboardTestBase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = self.make_user()
        self.client.force_login(self.user)

    def make_user(self, username='testuser', password='123456', is_staff=True, is_superuser=False):
        return User.objects.create_user(
            username=username,
            password=password,
            is_staff=is_staff,
            is_superuser=is_superuser
        )

    def make_category(self, name='Categoria Teste'):
        return Category.objects.create(name=name)

    def make_recipe(self, **kwargs):
        defaults = {
            'title': 'Receita Teste',
            'description': 'Descrição Teste',
            'slug': 'receita-teste',
            'preparation_time': 10,
            'preparation_time_unit': 'min',
            'servings': 2,
            'servings_unit': 'porcao',
            'preparation_steps': 'Passos de preparo',
            'preparation_steps_is_html': False,
            'cover': '',
            'category': self.make_category(),
            'author': self.user,
        }
        defaults.update(kwargs)
        return Recipe.objects.create(**defaults)

    def login(self, user=None):
        if user is None:
            user = self.user
        self.client.force_login(user)

    def logout(self):
        self.client.logout()

    def get_dashboard_url(self, name, **kwargs):
        from django.urls import reverse
        return reverse(f'dashboard:{name}', kwargs=kwargs)

    
