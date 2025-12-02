import pytest
from recipes.models import Recipe, Category, User
from recipes.serializers import RecipeSerializer, CategorySerializer

class TestRecipeSerializer:
    @pytest.mark.django_db
    def test_create(self):
        user = User.objects.create(username='user')
        category = Category.objects.create(name='Bolos')
        data = {
            'title': 'Bolo',
            'description': 'desc',
            'author': user.id,
            'category': category.id,
            'preparation_time': 10,
            'preparation_time_unit': 'min',
            'servings': 2,
            'servings_unit': 'porcao',
            'preparation_steps': 'passos',
        }
        serializer = RecipeSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        recipe = serializer.save()
        assert recipe.title == 'Bolo'
        assert recipe.preparation_time == 10
        assert recipe.servings == 2

    @pytest.mark.django_db
    def test_update(self):
        user = User.objects.create(username='user')
        category = Category.objects.create(name='Bolos')
        recipe = Recipe.objects.create(
            title='Bolo',
            description='desc',
            author=user,
            category=category,
            preparation_time=10,
            preparation_time_unit='min',
            servings=2,
            servings_unit='porcao',
            preparation_steps='passos',
            slug='bolo',
        )
        data = {
            'title': 'Bolo de Cenoura',
            'preparation_time': 20,
            'servings': 4,
        }
        serializer = RecipeSerializer(instance=recipe, data=data, partial=True)
        assert serializer.is_valid(), serializer.errors
        updated = serializer.save()
        assert updated.title == 'Bolo de Cenoura'
        assert updated.preparation_time == 20
        assert updated.servings == 4

    @pytest.mark.django_db
    def test_method_field(self):
        user = User.objects.create(username='user')
        category = Category.objects.create(name='Bolos')
        recipe = Recipe.objects.create(
            title='Bolo',
            description='desc',
            author=user,
            category=category,
            preparation_time=15,
            preparation_time_unit='min',
            servings=2,
            servings_unit='porcao',
            preparation_steps='passos',
            slug='bolo',
        )
        serializer = RecipeSerializer(recipe)
        assert serializer.data['preparation'] == '15 min'

    @pytest.mark.django_db
    def test_validate_defaults(self):
        user = User.objects.create(username='user')
        category = Category.objects.create(name='Bolos')
        recipe = Recipe.objects.create(
            title='Bolo',
            description='desc',
            author=user,
            category=category,
            preparation_time=10,
            preparation_time_unit='min',
            servings=2,
            servings_unit='porcao',
            preparation_steps='passos',
            slug='bolo',
        )
        data = {
            'title': 'Bolo',
            'description': 'desc',
            'author': user.id,
            'category': category.id,
            # 'preparation_time' e 'servings' omitidos
            'preparation_time_unit': 'min',
            'servings_unit': 'porcao',
            'preparation_steps': 'passos',
        }
        serializer = RecipeSerializer(instance=recipe, data=data, partial=True)
        assert serializer.is_valid(), serializer.errors
        validated = serializer.save()
        assert validated.preparation_time == 10
        assert validated.servings == 2

class TestCategorySerializer:
    @pytest.mark.django_db
    def test_category_serializer(self):
        category = Category.objects.create(name='Bolos')
        serializer = CategorySerializer(category)
        assert serializer.data['name'] == 'Bolos'
