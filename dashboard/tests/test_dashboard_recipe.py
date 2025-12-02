from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from recipes.models import Recipe, Category
from dashboard.forms.recipe_form import DashboardRecipeForm
from .test_dashboard_base import DashboardBaseTest

class DashboardRecipeViewTest(DashboardBaseTest):
	def setUp(self):
		self.user = self.create_superuser(username='admin', password='admin123')
		self.login_user(self.user)

	def test_get_new_recipe_returns_form(self):
		url = reverse('dashboard:dashboard_recipe_new')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'dashboard/pages/dashboard_recipe.html')
		self.assertIsInstance(response.context['form'], DashboardRecipeForm)

	def test_get_edit_recipe_returns_filled_form(self):
		category = Category.objects.create(name='Categoria')
		recipe = Recipe.objects.create(
			title='Receita',
			description='Desc',
			slug='receita',
			preparation_time=10,
			preparation_time_unit='min',
			servings=2,
			servings_unit='pessoas',
			preparation_steps='Passos',
			category=category,
			author=self.user,
			
		)
		url = reverse('dashboard:dashboard_recipe_edit', args=(recipe.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'dashboard/pages/dashboard_recipe.html')
		self.assertEqual(response.context['form'].instance, recipe)

	def test_get_edit_recipe_invalid_id_returns_404(self):
		url = reverse('dashboard:dashboard_recipe_edit', args=(9999,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)

	def test_post_valid_data_creates_recipe(self):
		category = Category.objects.create(name='NovaCat')
		url = reverse('dashboard:dashboard_recipe_new')
		data = {
			'title': 'Nova Receita',
			'description': 'Desc',
			'slug': 'nova-receita',
			'preparation_time': 10,
			'preparation_time_unit': 'min',
			'servings': 2,
			'servings_unit': 'pessoa',  # value valid
			'preparation_steps': 'Passos',
			'category': category.id,
			'author': self.user.id,
		}
		response = self.client.post(url, data, follow=True)
		self.assertContains(response, 'Sua receita foi salva com sucesso.')
		self.assertTemplateUsed(response, 'dashboard/pages/dashboard_recipe.html')

	def test_post_invalid_data_shows_form_with_errors(self):
		url = reverse('dashboard:dashboard_recipe_new')
		data = {'title': ''}  # Required title
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'dashboard/pages/dashboard_recipe.html')
		self.assertTrue(response.context['form'].errors)

	def test_delete_recipe_post_valid(self):
		category = Category.objects.create(name='Cat')
		recipe = Recipe.objects.create(
			title='Del',
			description='Desc',
			slug='del',
			preparation_time=10,
			preparation_time_unit='min',
			servings=2,
			servings_unit='pessoas',
			preparation_steps='Passos',
			category=category,
			author=self.user,
			
		)
		url = reverse('dashboard:dashboard_recipe_delete')
		data = {'id': recipe.id}
		response = self.client.post(url, data, follow=True)
		self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())
		self.assertContains(response, 'Sua receita foi deletada com sucesso.')

	def test_delete_recipe_post_invalid_id_returns_404(self):
		url = reverse('dashboard:dashboard_recipe_delete')
		data = {'id': 9999}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, 404)
