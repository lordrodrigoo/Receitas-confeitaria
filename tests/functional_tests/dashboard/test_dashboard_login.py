from .base import DashboardBaseTest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By

class DashboardLoginTest(DashboardBaseTest):
    def test_superuser_login(self):
        # create user and login using helpers
        self.create_superuser(username='admin', password='Admin123@!')
        self.login_as('admin', 'Admin123@!')
        body = self.browser.find_element(By.TAG_NAME, 'body')
        assert 'Você está logado.' in body.text

