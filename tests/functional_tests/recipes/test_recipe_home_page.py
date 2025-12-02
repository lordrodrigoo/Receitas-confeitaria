import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest.mock import patch
from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_home_page_shows_recipe_data(self):
        author = self.make_author(username='chef1')
        recipe = self.make_recipe(
            title='Bolo de Limão',
            slug='bolo-limao',
            author=author,
            description='Delicioso bolo cítrico',
            cover='recipes/covers/2025/10/28/cover.jpg',
            category=self.make_category(name='Bolos')
        )
        self.browser.get(self.live_server_url)
        self.sleep(2)
        card = self.browser.find_element(By.CLASS_NAME, 'recipe-list-item')
        card_text = card.text
        assert 'Bolo de Limão' in card_text
        assert 'chef1' in card_text
        assert 'Delicioso bolo cítrico' in card_text
        assert 'Bolos' in card_text
        # Checking the cover image
        img = card.find_element(By.TAG_NAME, 'img')
        assert 'cover.jpg' in img.get_attribute('src')


    def test_search_partial_and_case_insensitive(self):
        # Creating recipes
        self.make_recipe(title='Bolo de Chocolate', slug='bolo-chocolate', author=self.make_author(username='user10'))
        self.make_recipe(title='Bolo de Cenoura', slug='bolo-cenoura', author=self.make_author(username='user11'))

        self.browser.get(self.live_server_url)
        search_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Pesquisar receitas..."]')
        search_input.send_keys('bolo')
        search_input.send_keys(Keys.ENTER)
        self.sleep(2)
        page_text = self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
        assert 'Bolo de Chocolate' in page_text
        assert 'Bolo de Cenoura' in page_text

        # Test case-insensitive
        self.browser.get(self.live_server_url)
        search_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Pesquisar receitas..."]')
        search_input.send_keys('BOLO')
        search_input.send_keys(Keys.ENTER)
        self.sleep(2)
        page_text = self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
        assert 'Bolo de Chocolate' in page_text
        assert 'Bolo de Cenoura' in page_text

    def test_navigate_to_recipe_detail(self):
        # Create recipe
        recipe = self.make_recipe(title='Bolo de Laranja', slug='bolo-laranja', author=self.make_author(username='user12'))
        self.browser.get(self.live_server_url)
        self.sleep(2)
        # Click on the recipe title link
        link = self.browser.find_element(By.LINK_TEXT, 'Bolo de Laranja')
        link.click()
        self.sleep(2)
        # Check if on the detail page
        detail_title = self.browser.find_element(By.CSS_SELECTOR, 'h2.recipe-title a').text
        assert 'Bolo de Laranja' in detail_title

    def test_leia_mais_button_navigates_to_detail(self):
        recipe = self.make_recipe(title='Bolo de Coco', slug='bolo-coco', author=self.make_author(username='user13'))
        self.browser.get(self.live_server_url)
        self.sleep(2)
        leia_mais = self.browser.find_element(By.LINK_TEXT, 'Leia Mais...')
        leia_mais.click()
        self.sleep(2)
        detail_title = self.browser.find_element(By.CSS_SELECTOR, 'h2.recipe-title a').text
        assert 'Bolo de Coco' in detail_title


    @patch('recipes.views.site.PER_PAGE', new=9)
    def test_home_page_pagination(self):
        # Create 12 recipes to test pagination
        self.make_recipe_in_batch(qtd=12)

        self.browser.get(self.live_server_url)
        self.sleep(2)

        # Check if pagination controls exist
        pagination = self.browser.find_element(By.CLASS_NAME, 'pagination')
        assert pagination is not None

        # Check if only 9 recipes appear on the first page
        recipes_list = self.browser.find_elements(By.CLASS_NAME, 'recipe-list-item')
        assert len(recipes_list) == 9

    def test_search_field_finds_recipe(self):
        # Create two recipes with unique authors
        title1 = 'Bolo de Cenoura'
        title2 = 'Torta de Limão'
        self.make_recipe(title=title1, slug='bolo-cenoura', author=self.make_author(username='user1'))
        self.make_recipe(title=title2, slug='torta-limao', author=self.make_author(username='user2'))

        self.browser.get(self.live_server_url)
        search_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Pesquisar receitas..."]')
        search_input.send_keys(title1)
        search_input.send_keys(Keys.ENTER)

        self.sleep(2)
        page_text = self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
        assert title1 in page_text
        assert title2 not in page_text

    def test_home_page_shows_no_recipes_message(self):
            self.browser.get(self.live_server_url)
            self.sleep(2)
            page_text = self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
            assert 'Não encontramos receitas aqui! 😢' in page_text

    def test_home_page_lists_recipes(self):
            # Create 3 recipes with unique authors
            for i in range(3):
                    self.make_recipe(
                            title=f'Receita {i+1}',
                            slug=f'receita-{i+1}',
                            author=self.make_author(username=f'user{i+1}')
                    )

            self.browser.get(self.live_server_url)
            self.sleep(2)
            page_text = self.browser.find_element(By.CLASS_NAME, 'main-content-list').text

            assert 'Receita 1' in page_text
            assert 'Receita 2' in page_text
            assert 'Receita 3' in page_text