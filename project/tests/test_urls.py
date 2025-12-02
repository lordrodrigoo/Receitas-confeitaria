import pytest
from django.urls import reverse, resolve
from django.conf import settings

class TestProjectUrls:
    def test_admin_url(self):
        url = reverse('admin:index')
        match = resolve(url)
        assert match is not None

    def test_recipes_home(self):
        url = reverse('recipes:home')
        match = resolve(url)
        assert match is not None

    def test_dashboard(self):
        url = reverse('dashboard:dashboard')
        match = resolve(url)
        assert match is not None

    def test_static_url(self):
        url = settings.STATIC_URL
        assert url.startswith('/static/')

    def test_media_url(self):
        url = settings.MEDIA_URL
        assert url.startswith('/media/')

    def test_project_urls_resolve(self):
        url_names = [
            'recipes:home',
            'dashboard:dashboard',
            'dashboard:dashboard_category_delete',
            'dashboard:dashboard_user_delete',
            'recipes:recipe',
        ]
        for name in url_names:
            if name == 'recipes:recipe':
                url = reverse(name, args=[1])
            else:
                url = reverse(name)
            match = resolve(url)
            assert match is not None


