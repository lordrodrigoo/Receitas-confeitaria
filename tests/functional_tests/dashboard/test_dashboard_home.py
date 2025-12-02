import pytest
from selenium.webdriver.common.by import By
from .dashboard_base import DashboardBaseFunctionalTest


@pytest.mark.functional_test
class DashboardHomeFunctionalTest(DashboardBaseFunctionalTest):
    
    def test_superuser_can_login_dashboard(self):
        # Create user and make superuser
        superuser = self.make_author(username='maria', password='MARIA123456@!')
        superuser.is_active = True
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save()
        self.login_dashboard_user('maria', 'MARIA123456@')
        
        assert 'Painel de Controle' in self.browser.page_source

    def test_superuser_can_create_recipe(self):
        # Login superuser
        superuser = self.make_author(username='admin2', password='admin123@!')
        superuser.is_active = True
        superuser.is_superuser = True
        superuser.is_staff = True
        superuser.save()
        self.login_dashboard_user('admin2', 'admin123@!')
        # Create recipe using utility method
        self.create_recipe_dashboard(
            titulo='Receita Teste',
            descricao='Descrição da receita teste.',
            tempo_preparo='10',
            unidade_tempo='Minutos',
            rendimento='2',
            unidade_rendimento='Porções',
            modo_preparo='Modo de preparo teste.',
            categoria=None,  # Select the first available option
            autor=None,      # Select the first author shown
            cover_path=None  # Don't upload cover image
        )
        # Check if success message or recipe appears in the listing
        assert 'Receita Teste' in self.browser.page_source or 'Receita criada' in self.browser.page_source


