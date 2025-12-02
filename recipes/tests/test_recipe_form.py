import pytest
from recipes.forms.recipe_form import RecipeForm
from recipes.models import Category

class RecipeFormTestBase:
	def make_data(self, **kwargs):
		data = {
			'title': 'Bolo',
			'description': 'desc',
			'slug': 'bolo',
			'preparation_time': 10,
			'preparation_time_unit': 'min',
			'servings': 2,
			'servings_unit': 'porcao',
			'preparation_steps': 'passos',
			'preparation_steps_is_html': False,
			'cover': '',
			'category': '',
			'new_category': '',
		}
		data.update(kwargs)
		return data

	def create_category(self, name='Bolos'):
		return Category.objects.create(name=name)

class TestRecipeForm(RecipeFormTestBase):
	@pytest.mark.django_db
	def test_no_category_or_new_category(self):
		form = RecipeForm(data=self.make_data())
		assert not form.is_valid()
		assert 'Escolha uma categoria existente ou crie uma nova.' in str(form.errors)

	@pytest.mark.django_db
	def test_existing_category_only(self):
		category = self.create_category()
		form = RecipeForm(data=self.make_data(category=category.id))
		assert form.is_valid()

	@pytest.mark.django_db
	def test_new_category_only(self):
		form = RecipeForm(data=self.make_data(new_category='Nova'))
		assert form.is_valid()

	@pytest.mark.django_db
	def test_both_category_and_new_category(self):
		category = self.create_category()
		form = RecipeForm(data=self.make_data(category=category.id, new_category='Nova'))
		assert form.is_valid()
