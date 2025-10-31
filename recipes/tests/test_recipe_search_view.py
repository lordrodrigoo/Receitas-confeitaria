from django.urls import reverse, resolve
from .test_recipe_base import RecipeTestBase
from recipes.views import site

class RecipeSearchViewTest(RecipeTestBase):
    def test_search_url_returns_200(self):
        response = self.client.get(reverse('recipes:search') + '?q=bolo')
        assert response.status_code == 200


    def test_recipe_search_uses_correct_view_function(self):
        resolved_view = resolve(reverse('recipes:search'))
        self.assertIs(resolved_view.func.view_class, site.RecipeListViewSearch)

    def test_recipe_search_raises_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


    def test_search_no_results_shows_not_found_message(self):
        url = reverse('recipes:search') + '?q=teste1234'
        response = self.client.get(url)
        self.assertContains(response, 'Não encontramos receitas aqui! 😢')

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            title=title1,
            slug='recipe-one',
            is_published=True,
        )

        recipe2 = self.make_recipe(
            title=title2,
            slug='recipe-two',
            is_published=True,
        )
        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=This')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])

