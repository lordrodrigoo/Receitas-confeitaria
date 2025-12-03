from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User
from typing import Optional

class DashboardBaseTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = make_chrome_browser()
        return super().setUp()
    
    def tearDown(self):
        self.browser.quit()
        return super().tearDown()
    
    def sleep(self, qtd=5):
        time.sleep(qtd)

    # Wait helpers
    def wait_for_element(self, by, locator, timeout=10):
        return WebDriverWait(self.browser, timeout).until(
            EC.presence_of_element_located((by, locator))
        )

    def wait_for_element_visible(self, by, locator, timeout=10):
        return WebDriverWait(self.browser, timeout).until(
            EC.visibility_of_element_located((by, locator))
        )

    def wait_for_text_in_body(self, text, timeout=10):
        return WebDriverWait(self.browser, timeout).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), text)
        )

    def wait_for_url_contains(self, path_fragment, timeout=10):
        return WebDriverWait(self.browser, timeout).until(
            lambda b: path_fragment in b.current_url
        )

    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH, f'//input[@placeholder="{placeholder}"]')
    

    # Helper: create and return a superuser
    def create_superuser(self, username: str = 'admin', password: str = 'Admin123@!') -> User:
        return User.objects.create_superuser(username=username, password=password)

    # Helper: perform login via dashboard login form
    def login_as(self, username: str, password: str, wait: int = 2):
        """Open the dashboard login page and authenticate the given user."""
        self.browser.get(self.live_server_url + '/dashboard/login')
        self.browser.find_element(By.NAME, 'usuario').send_keys(username)
        self.browser.find_element(By.NAME, 'senha').send_keys(password)
        # Click the submit button inside the login form specifically
        submit_xpath = '//input[@name="usuario"]/ancestor::form[1]//button[@type="submit"]'
        self.browser.find_element(By.XPATH, submit_xpath).click()
        # wait until the dashboard url is loaded (or login message shows)
        try:
            self.wait_for_url_contains('/dashboard/dashboard', timeout=wait)
        except Exception:
            # fallback: wait for login message text to appear
            self.wait_for_text_in_body('Você está logado.', timeout=wait)

    # Helper: click the "Criar receita" link in the dashboard menu
    def go_to_create_recipe(self, wait: int = 1):
        self.browser.find_element(By.LINK_TEXT, 'Criar receita').click()
        # wait for recipe form to be present
        self.wait_for_element_visible(By.NAME, 'title', timeout=wait)

    # Helper: fills the recipe form using provided values
    def fill_recipe_form(
        self,
        title: str,
        description: str,
        preparation_time: str,
        preparation_time_unit: str,
        servings: str,
        servings_unit: str,
        preparation_steps: str,
        new_category: Optional[str] = None,
        new_author: Optional[str] = None,
    ):
        self.browser.find_element(By.NAME, 'title').send_keys(title)
        self.browser.find_element(By.NAME, 'description').send_keys(description)
        self.browser.find_element(By.NAME, 'preparation_time').send_keys(preparation_time)
        self.browser.find_element(By.NAME, 'preparation_time_unit').send_keys(preparation_time_unit)
        self.browser.find_element(By.NAME, 'servings').send_keys(servings)
        self.browser.find_element(By.NAME, 'servings_unit').send_keys(servings_unit)
        self.browser.find_element(By.NAME, 'preparation_steps').send_keys(preparation_steps)
        if new_category:
            self.browser.find_element(By.NAME, 'new_category').send_keys(new_category)
        if new_author:
            self.browser.find_element(By.NAME, 'new_author').send_keys(new_author)

    # Helper: submits the form that contains the given field name (default 'title')
    def submit_form_containing(self, field_name: str = 'title', wait: int = 2):
        submit_form_xpath = f'//input[@name="{field_name}"]/ancestor::form[1]//button[@type="submit"]'
        self.browser.find_element(By.XPATH, submit_form_xpath).click()
        # wait for success message or redirect
        self.wait_for_text_in_body('Sua receita foi salva com sucesso.', timeout=wait)

    # Helper: click 'Minhas receitas' to go to dashboard list
    def go_to_dashboard(self, wait: int = 1):
        self.browser.find_element(By.LINK_TEXT, 'Minhas receitas').click()
        # wait for dashboard list to be visible
        self.wait_for_element_visible(By.CLASS_NAME, 'dashboard-table', timeout=wait)

    # Helper: perform logout by clicking the logout button in the dashboard menu
    def logout_user(self, wait: int = 1):
        logout_btn = self.browser.find_element(By.CLASS_NAME, 'dashboard-menu-logout')
        logout_btn.click()
        # wait for logout success message
        self.wait_for_text_in_body('Logout realizado com sucesso.', timeout=wait)
    
    
