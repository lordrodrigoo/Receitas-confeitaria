import pytest
from django.urls import reverse


def test_recipe_home_view_returns_status_code_200_OK(client):
        response = client.get(reverse('home'))
        assert response.status_code == 200