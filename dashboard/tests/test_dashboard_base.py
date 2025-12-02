from django.test import TestCase
from django.contrib.auth import get_user_model




class DashboardBaseTest(TestCase):
    def create_user(self, **kwargs):
        return get_user_model().objects.create_user(**kwargs)
    
    def create_superuser(self, **kwargs):
        return get_user_model().objects.create_superuser(**kwargs)
    
    def login_user(self, user):
        self.client.force_login(user)

    def create_category(self, name='Categoria'):
        ... # Implementation for creating a category

    def create_recipe(self, **kwargs):
        ... # Implementation for creating a recipe

    