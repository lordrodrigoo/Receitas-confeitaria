from .base import DashboardBaseTest
from selenium.webdriver.common.by import By

class DashboardSuperUserTests(DashboardBaseTest):
    def setUp(self):
        super().setUp()
        self.super_username = 'superuser'
        self.super_password = 'Super123@!'
        self.create_superuser(username=self.super_username, password=self.super_password)
        self.login_as(self.super_username, self.super_password)

    
    def test_super_user_add_new_user(self):
        # Click on the "Add user" menu
        self.browser.find_element(By.LINK_TEXT, 'Adicionar usuário').click()
        self.wait_for_element_visible(By.NAME, 'username')

        self.browser.find_element(By.NAME, 'first_name').send_keys('Novo')
        self.browser.find_element(By.NAME, 'last_name').send_keys('Usuário')
        self.browser.find_element(By.NAME, 'username').send_keys('novouser')
        self.browser.find_element(By.NAME, 'email').send_keys('novouser@example.com')
        self.browser.find_element(By.NAME, 'password').send_keys('User12345!')

        submit_xpath = '//input[@name="username"]/ancestor::form[1]//button[@type="submit"]'
        self.browser.find_element(By.XPATH, submit_xpath).click()
        # wait for redirect to dashboard
        self.wait_for_url_contains('/dashboard')
        # wait for success message
        self.wait_for_message('Usuário criado com sucesso!')


    def test_super_user_edit_new_user(self):
        user = self.create_user(username='edituser', password='Edit12345!')
        # Refresh the dashboard to ensure the user appears in the table
        self.browser.refresh()
        self.wait_for_text_in_body(user.username)
        user_row_xpath = f"//div[h3[contains(text(), 'Usuários')]]//tr[td[contains(text(), '{user.username}')]]"
        edit_btn = self.browser.find_element(By.XPATH, user_row_xpath + "//a[@class='btn-edit' and @title='Editar']")
        edit_btn.click()
        self.wait_for_element_visible(By.NAME, 'email')
        email_field = self.browser.find_element(By.NAME, 'email')
        email_field.clear()
        email_field.send_keys('edituser@example.com')
        submit_xpath = "//input[@name='email']/ancestor::form[1]//button[@type='submit']"
        self.browser.find_element(By.XPATH, submit_xpath).click()
        self.wait_for_message('Usuário editado com sucesso!')

    def test_super_user_delete_user(self):
        user = self.create_user(username='deleteuser', password='Delete12345!')
        self.browser.refresh()
        self.wait_for_text_in_body(user.username)
        user_row_xpath = f"//div[h3[contains(text(), 'Usuários')]]//tr[td[contains(text(), '{user.username}')]]"
        delete_btn = self.browser.find_element(By.XPATH, user_row_xpath + "//button[@class='btn-delete' and @title='Excluir']")
        delete_btn.click()
        # Accept the confirmation alert
        self.browser.switch_to.alert.accept()
        self.wait_for_message('Usuário excluído com sucesso!')
    
    

    def test_super_user_edit_category(self):
        category = self.create_category(name='Categoria Editar')
        self.browser.refresh()
        self.wait_for_text_in_body(category.name)
        category_row_xpath = f"//div[h3[contains(text(), 'Categorias')]]//tr[td[contains(text(), '{category.name}')]]"
        edit_btn = self.browser.find_element(By.XPATH, category_row_xpath + "//a[@class='btn-edit' and @title='Editar']")
        edit_btn.click()
        self.wait_for_element_visible(By.NAME, 'name')
        name_field = self.browser.find_element(By.NAME, 'name')
        name_field.clear()
        name_field.send_keys('Categoria Editada')
        submit_xpath = "//input[@name='name']/ancestor::form[1]//button[@type='submit']"
        self.browser.find_element(By.XPATH, submit_xpath).click()
        self.wait_for_message('Categoria editada com sucesso!')
    
    def test_super_user_delete_category(self):
        category = self.create_category(name='Categoria Excluir')
        self.browser.refresh()
        self.wait_for_text_in_body(category.name)
        category_row_xpath = f"//div[h3[contains(text(), 'Categorias')]]//tr[td[contains(text(), '{category.name}')]]"
        delete_btn = self.browser.find_element(By.XPATH, category_row_xpath + "//button[@class='btn-delete' and @title='Excluir']")
        delete_btn.click()
        # Accept the confirmation alert
        self.browser.switch_to.alert.accept()
        self.wait_for_message('Categoria excluída com sucesso!')

    def test_super_user_access_dashboard(self):
        body = self.browser.find_element(By.TAG_NAME, 'body')
        assert 'Você está logado.' in body.text

    def test_super_user_logout(self):
        self.logout_user()
        self.wait_for_url_contains('/dashboard/login')
        self.wait_for_message('Logout realizado com sucesso.')