import os
import tempfile
import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from recipes.models import Recipe

@pytest.mark.django_db
def test_resize_image_reduces_width(tmp_path, settings):
    media_root = tmp_path / "media"
    media_root.mkdir()
    settings.MEDIA_ROOT = str(media_root)

    img_path = media_root / "test.jpg"
    image = Image.new('RGB', (1200, 600), color='red')
    image.save(img_path)

    uploaded = SimpleUploadedFile("test.jpg", img_path.read_bytes(), content_type="image/jpeg")
    uploaded.name = "test.jpg"

    Recipe.resize_image(uploaded, new_width=800)

    img = Image.open(img_path)
    assert img.width == 800
    assert img.height == round((800 * 600) / 1200)
    img.close()

@pytest.mark.django_db
def test_resize_image_smaller_width(tmp_path, settings):
    media_root = tmp_path / "media"
    media_root.mkdir()
    settings.MEDIA_ROOT = str(media_root)

    img_path = media_root / "small.jpg"
    image = Image.new('RGB', (400, 200), color='blue')
    image.save(img_path)

    uploaded = SimpleUploadedFile("small.jpg", img_path.read_bytes(), content_type="image/jpeg")
    uploaded.name = "small.jpg"

    Recipe.resize_image(uploaded, new_width=800)

    img = Image.open(img_path)
    assert img.width == 400
    assert img.height == 200
    img.close()
