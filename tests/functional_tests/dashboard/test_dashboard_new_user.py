from .base import DashboardBaseTest
from selenium.webdriver.common.by import By

class DashboardAddUserTest(DashboardBaseTest):
    def setUp(self):
        super().setUp()
        self.user_username = 'novouser'
        self.user_password = 'User12345!'
        self.user = self.create_user(username=self.user_username, password=self.user_password)
        self.superuser = self.create_superuser(username='admin', password='Admin123@!')
        self.login_as(self.user_username, self.user_password)

    def test_user_can_create_recipe(self):
        self.go_to_create_recipe()
        self.fill_recipe_form(
            title='Bolo de Teste',
            description='Receita de teste',
            preparation_time='30',
            preparation_time_unit='minutos',
            servings='10',
            servings_unit='fatias',
            preparation_steps='Misture tudo e asse.',
            new_category='Categoria Teste',
            new_author=self.user_username
        )
        self.submit_form_containing('title')
        self.wait_for_text_in_body('Sua receita foi salva com sucesso.')

    def test_user_can_edit_own_recipe(self):
        from recipes.models import Recipe
        recipe = Recipe.objects.create(
            title='Receita Editável',
            description='desc',
            preparation_time=10,
            preparation_time_unit='minutos',
            servings=2,
            servings_unit='porções',
            preparation_steps='passos',
            author=self.user
        )
        self.go_to_dashboard()
        self.browser.find_element(By.LINK_TEXT, recipe.title).click()
        self.wait_for_element_visible(By.NAME, 'title')
        title_field = self.browser.find_element(By.NAME, 'title')
        title_field.clear()
        title_field.send_keys('Receita Editada')
        new_category_field = self.browser.find_element(By.NAME, 'new_category')
        new_category_field.clear()
        new_category_field.send_keys('Categoria Editada')
        new_author_field = self.browser.find_element(By.NAME, 'new_author')
        new_author_field.clear()
        new_author_field.send_keys(self.user_username)
        self.submit_form_containing('title')
        self.wait_for_text_in_body('Sua receita foi salva com sucesso.')

    def test_user_can_delete_own_recipe(self):
        from recipes.models import Recipe
        recipe = Recipe.objects.create(
            title='Receita Deletável',
            description='desc',
            preparation_time=10,
            preparation_time_unit='minutos',
            servings=2,
            servings_unit='porções',
            preparation_steps='passos',
            author=self.user
        )
        self.go_to_dashboard()
        row_xpath = f"//tr[td/a[text()='{recipe.title}']]"
        delete_btn = self.browser.find_element(By.XPATH, row_xpath + "//button[@class='btn-delete' and @title='Excluir']")
        delete_btn.click()
        self.browser.switch_to.alert.accept()
        self.wait_for_text_in_body('Sua receita foi deletada com sucesso.')

    def test_user_cannot_delete_superuser(self):
        self.go_to_dashboard()
        admin_row_xpath = "//div[h3[contains(text(), 'Usuários')]]//tr[td[contains(text(), 'admin')]]"
        delete_buttons = self.browser.find_elements(By.XPATH, admin_row_xpath + "//button[@class='btn-delete' and @title='Excluir']")
        assert len(delete_buttons) == 0, 'Usuário comum não deve ver botão de deletar superusuário'



    

