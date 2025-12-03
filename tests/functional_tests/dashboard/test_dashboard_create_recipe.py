from .base import DashboardBaseTest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By


class DashboardCreateRecipeTest(DashboardBaseTest):
    def test_superuser_can_create_recipe(self):
        # create superuser and login using helpers
        self.create_superuser(username='admin', password='Admin123@!')
        self.login_as('admin', 'Admin123@!')

        # go to recipe creation
        self.go_to_create_recipe()

        # Fill out the recipe form using helper
        self.fill_recipe_form(
            title='Bolo de Chocolate',
            description='Delicioso bolo de chocolate.',
            preparation_time='60',
            preparation_time_unit='min',
            servings='8',
            servings_unit='pessoas',
            preparation_steps='Misture tudo e asse por 60 minutos.',
            new_category='Bolos',
            new_author='autor_teste',
        )
        # submit form
        self.submit_form_containing('title')

        body = self.browser.find_element(By.TAG_NAME, 'body')
        assert 'Sua receita foi salva com sucesso.' in body.text

    def test_superuser_sees_created_recipe_in_dashboard(self):
        # create superuser and login using helpers
        self.create_superuser(username='admin2', password='Admin123@!')
        self.login_as('admin2', 'Admin123@!')

        # go to create recipe
        self.go_to_create_recipe()

        # fill form and submit via helpers
        title = 'Biscoito de Aveia'
        self.fill_recipe_form(
            title=title,
            description='Biscoito saudável.',
            preparation_time='20',
            preparation_time_unit='min',
            servings='12',
            servings_unit='pessoas',
            preparation_steps='Misture e asse por 20 minutos.',
            new_category='Biscoitos',
            new_author='autor_teste2',
        )
        self.submit_form_containing('title')

        # go to dashboard list and verify the recipe title appears
        self.go_to_dashboard()
        body = self.browser.find_element(By.TAG_NAME, 'body')
        assert title in body.text
