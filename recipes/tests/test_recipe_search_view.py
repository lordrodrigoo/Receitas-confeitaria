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

    