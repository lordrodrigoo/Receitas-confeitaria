import re
from .base import DashboardBaseTest
from selenium.webdriver.common.by import By


class DashboardEditDeleteRecipeTest(DashboardBaseTest):
    def test_superuser_can_edit_recipe(self):
        # superuser creates and logs in
        self.create_superuser(username='editor', password='Admin123@!')
        self.login_as('editor', 'Admin123@!')

        # create recipe
        original_title = 'Pudim Simples'
        self.go_to_create_recipe()
        self.fill_recipe_form(
            title=original_title,
            description='Pudim delicioso.',
            preparation_time='90',
            preparation_time_unit='min',
            servings='6',
            servings_unit='pessoas',
            preparation_steps='Misture e leve ao forno.',
            new_category='Sobremesas',
            new_author='editor'
        )
        # after submit, we are on the recipe edit page
        self.submit_form_containing('title')

        # edit the title
        new_title = 'Pudim de Leite'
        title_field = self.browser.find_element(By.NAME, 'title')
        title_field.clear()
        title_field.send_keys(new_title)
        self.submit_form_containing('title')

        # verify success message and presence of the new title in the listing
        self.go_to_dashboard()
        body = self.browser.find_element(By.TAG_NAME, 'body')
        assert new_title in body.text

    def test_superuser_can_delete_recipe(self):
        # superuser creates and logs in
        self.create_superuser(username='deleter', password='Admin123@!')
        self.login_as('deleter', 'Admin123@!')

        # create recipe to delete
        title = 'Bolo Para Deletar'
        self.go_to_create_recipe()
        self.fill_recipe_form(
            title=title,
            description='Será apagado.',
            preparation_time='30',
            preparation_time_unit='min',
            servings='4',
            servings_unit='pessoas',
            preparation_steps='Assar.',
            new_category='Testes',
            new_author='deleter'
        )
        self.submit_form_containing('title')

        # extract id from current URL (we expect to be at /dashboard/recipe/<id>/edit/)
        current = self.browser.current_url
        m = re.search(r'/dashboard/recipe/(\d+)/', current)
        assert m, f'Could not find recipe id in url: {current}'
        recipe_id = m.group(1)

        # go to the dashboard and find the delete form for that id
        self.go_to_dashboard()
        delete_form_xpath = f'//input[@type="hidden" and @name="id" and @value="{recipe_id}"]/ancestor::form[1]'
        form = self.browser.find_element(By.XPATH, delete_form_xpath)
        # click the delete button inside the form (there is a JS confirm)
        btn = form.find_element(By.XPATH, './/button[@type="submit"]')
        btn.click()

        # accept the confirm if it appears
        try:
            alert = self.browser.switch_to.alert
            alert.accept()
        except Exception:
            # if there is no alert, continue
            pass

        # wait for success message and verify removal from the listing
        self.wait_for_text_in_body('Sua receita foi deletada com sucesso.')
        body = self.browser.find_element(By.TAG_NAME, 'body')
        assert title not in body.text
