from selenium.webdriver.common.by import By
from tests.functional_tests.recipes.base import RecipeBaseFunctionalTest

class DashboardBaseFunctionalTest(RecipeBaseFunctionalTest):
   
    def login_dashboard_user(self, username, password):
        self.browser.get(self.live_server_url + '/dashboard/login/')
        self.browser.find_element(By.NAME, 'username').send_keys(username)
        self.browser.find_element(By.NAME, 'password').send_keys(password)
        self.browser.find_element(By.XPATH, '//button[@type="submit"]').click()
        self.sleep(1)


