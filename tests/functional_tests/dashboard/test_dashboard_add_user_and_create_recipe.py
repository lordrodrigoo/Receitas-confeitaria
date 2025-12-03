from .base import DashboardBaseTest
from selenium.webdriver.common.by import By


class DashboardAddUserAndCreateRecipeTest(DashboardBaseTest):
    def test_superuser_adds_user_and_new_user_creates_recipe(self):
        # create superuser and login
        self.create_superuser(username='super', password='Admin123@!')
        self.login_as('super', 'Admin123@!')

        # go to add person page (link visible only to superusers)
        self.browser.find_element(By.LINK_TEXT, 'Adicionar usuário').click()
        # wait for the add person form
        self.wait_for_element_visible(By.NAME, 'username')

        # fill add person form
        new_username = 'newuser'
        new_password = 'User12345!'
        self.browser.find_element(By.NAME, 'first_name').send_keys('New')
        self.browser.find_element(By.NAME, 'last_name').send_keys('User')
        self.browser.find_element(By.NAME, 'username').send_keys(new_username)
        self.browser.find_element(By.NAME, 'email').send_keys('newuser@example.com')
        # password field exists on the form
        self.browser.find_element(By.NAME, 'password').send_keys(new_password)

        # submit add person form and wait for success message
        submit_xpath = '//input[@name="username"]/ancestor::form[1]//button[@type="submit"]'
        self.browser.find_element(By.XPATH, submit_xpath).click()
        self.wait_for_text_in_body('Usuário criado com sucesso!')

        # logout superuser
        self.logout_user()

        # login as the new user
        self.login_as(new_username, new_password)

        # go to create recipe
        self.go_to_create_recipe()

        # fill and submit recipe form
        title = 'Torta de Maçã'
        self.fill_recipe_form(
            title=title,
            description='Torta caseira de maçã.',
            preparation_time='50',
            preparation_time_unit='min',
            servings='6',
            servings_unit='pessoas',
            preparation_steps='Misture, recheie e asse por 50 minutos.',
            new_category='Tortas',
            new_author='newuser'
        )
        # use the recipe-specific submit helper (it waits for success message)
        self.submit_form_containing('title')

        # verify recipe appears in dashboard list
        self.go_to_dashboard()
        body = self.browser.find_element(By.TAG_NAME, 'body')
        assert title in body.text
