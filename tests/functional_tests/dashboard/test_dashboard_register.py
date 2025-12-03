from .base import DashboardBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class DashboardRegisterTest(DashboardBaseTest):
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        # wait for the register form to be present and return it
        self.wait_for_element_visible(By.XPATH, '/html/body/main/div[2]/form', timeout=8)
        return self.browser.find_element(By.XPATH, '/html/body/main/div[2]/form')
    
    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/dashboard/register/')
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        callback(form)
        return form

    
    