from selenium.webdriver.common.by import By
from tests.functional_tests.recipes.base import RecipeBaseFunctionalTest

class DashboardBaseFunctionalTest(RecipeBaseFunctionalTest):
    def login_dashboard_user(self, username, password):
        self.browser.get(self.live_server_url + '/dashboard/login/')
        self.sleep(1)
        print(self.browser.page_source)  # Depuração: mostra HTML da página de login
        self.browser.find_element(By.NAME, 'usuario').send_keys(username)
        self.browser.find_element(By.NAME, 'senha').send_keys(password)
        try:
            self.browser.find_element(By.XPATH, '//button[text()="Enviar"]').click()
        except Exception:
            try:
                self.browser.find_element(By.XPATH, '//button[text()="Entrar"]').click()
            except Exception:
                self.browser.find_element(By.XPATH, '//button[@type="submit"]').click()
        self.sleep(1)

    def create_recipe_dashboard(self,
        titulo,
        descricao,
        tempo_preparo,
        unidade_tempo,
        rendimento,
        unidade_rendimento,
        modo_preparo,
        categoria=None,
        autor=None,
        cover_path=None
    ):
        self.browser.get(self.live_server_url + '/dashboard/dashboard/recipe/new/')
        self.sleep(1)
        print(self.browser.page_source)  # Depuração: mostra HTML da página de criação de receita

        def fill_by_names(names, value):
            for name in names:
                try:
                    self.browser.find_element(By.NAME, name).send_keys(value)
                    return True
                except Exception:
                    continue
            print(f'Campo não encontrado: {names}')
            return False

        fill_by_names(['titulo', 'title', 'nome'], titulo)
        fill_by_names(['descricao', 'description'], descricao)
        fill_by_names(['tempo_preparo', 'preparation_time', 'tempo'], tempo_preparo)
        fill_by_names(['unidade_tempo', 'preparation_time_unit', 'minutos'], unidade_tempo)
        fill_by_names(['rendimento', 'servings'], rendimento)
        fill_by_names(['unidade_rendimento', 'servings_unit', 'porcoes'], unidade_rendimento)
        fill_by_names(['modo_preparo', 'preparation', 'instructions'], modo_preparo)

        # Campo search (caso apareça indevidamente)
        fill_by_names(['search'], 'teste')

        # Categoria (select ou novo)
        if categoria:
            fill_by_names(['categoria', 'category'], categoria)
        else:
            try:
                select = self.browser.find_element(By.NAME, 'categoria')
                for option in select.find_elements(By.TAG_NAME, 'option'):
                    if option.text.strip() and option.get_attribute('value'):
                        option.click()
                        break
            except Exception:
                print('Categoria não encontrada ou não selecionada.')

        # Autor (select ou novo)
        if autor:
            fill_by_names(['autor', 'author'], autor)
        else:
            try:
                select = self.browser.find_element(By.NAME, 'autor')
                for option in select.find_elements(By.TAG_NAME, 'option'):
                    if option.text.strip() and option.get_attribute('value'):
                        option.click()
                        break
            except Exception:
                print('Autor não encontrado ou não selecionado.')

        # Cover (imagem)
        if cover_path:
            try:
                self.browser.find_element(By.NAME, 'cover').send_keys(cover_path)
            except Exception:
                print('Campo cover não encontrado ou erro ao enviar imagem.')

        try:
            self.browser.find_element(By.XPATH, '//button[@type="submit"]').click()
        except Exception:
            try:
                self.browser.find_element(By.XPATH, "//button[contains(text(), 'Enviar')]").click()
            except Exception:
                print('Botão de submit não encontrado!')
        self.sleep(2)
        print('HTML após submit:', self.browser.page_source)
