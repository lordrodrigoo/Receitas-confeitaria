import pytest
from unittest.mock import patch, MagicMock
from recipes.models import Recipe
from django.core.files.base import ContentFile
import os
from io import BytesIO
from PIL import Image

@pytest.mark.django_db
def test_recipe_cover_delete_signal_removes_file(tmp_path):
    with patch('os.remove') as mock_remove:
        # Cria uma imagem JPEG válida em memória
        img_io = BytesIO()
        image = Image.new('RGB', (10, 10), color='red')
        image.save(img_io, format='JPEG')
        img_io.seek(0)
        cover_file = ContentFile(img_io.read(), 'cover.jpg')
        recipe = Recipe.objects.create(
            title='Test',
            slug='test',
            cover=cover_file,
            preparation_time=10,
            preparation_time_unit='minutos',
            servings=2,
            servings_unit='porções',
            description='desc',
            category_id=None,
        )
        cover_path = recipe.cover.path
        # Assurance that the file exists before deletion
        assert os.path.exists(cover_path)
        recipe.delete()
        mock_remove.assert_called_once_with(cover_path)

@pytest.mark.django_db
def test_recipe_cover_update_signal_removes_old_cover(tmp_path):
    with patch('os.remove') as mock_remove:
        # Create a valid JPEG image in memory
        img_io = BytesIO()
        image = Image.new('RGB', (10, 10), color='blue')
        image.save(img_io, format='JPEG')
        img_io.seek(0)
        cover_file = ContentFile(img_io.read(), 'cover1.jpg')
        recipe = Recipe.objects.create(
            title='Test',
            slug='test',
            cover=cover_file,
            preparation_time=10,
            preparation_time_unit='minutos',
            servings=2,
            servings_unit='porções',
            description='desc',
            category_id=None,
        )
        old_cover_path = recipe.cover.path
        assert os.path.exists(old_cover_path)
        # Create a new valid image for update
        img_io2 = BytesIO()
        image2 = Image.new('RGB', (10, 10), color='green')
        image2.save(img_io2, format='JPEG')
        img_io2.seek(0)
        new_cover_file = ContentFile(img_io2.read(), 'cover2.jpg')
        recipe.cover = new_cover_file
        recipe.save()
        mock_remove.assert_called_once_with(old_cover_path)

@pytest.mark.django_db
def test_recipe_cover_update_signal_no_old_cover():
    with patch('os.remove') as mock_remove:
        recipe = Recipe(
            title='Test',
            slug='test',
            preparation_time=10,
            preparation_time_unit='minutos',
            servings=2,
            servings_unit='porções',
            description='desc',
            category_id=None,
        )
        # Does not save, so there is no old cover
        recipe.save()
        assert not mock_remove.called

@pytest.mark.django_db
def test_delete_cover_handles_file_not_found():
    from recipes import signals
    instance = MagicMock()
    instance.cover.path = '/tmp/nonexistent.jpg'
    with patch('os.remove', side_effect=FileNotFoundError):
        signals.delete_cover(instance)  # Não deve lançar
    with patch('os.remove', side_effect=ValueError):
        signals.delete_cover(instance)  # Não deve lançar
