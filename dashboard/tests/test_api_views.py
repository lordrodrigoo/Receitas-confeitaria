import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

@pytest.mark.django_db
def test_api_list_authenticated():
    User = get_user_model()
    user = User.objects.create_user('apiuser', 'apiuser@test.com', 'Abc12345')
    client = APIClient()
    client.force_authenticate(user=user)
    url = '/dashboard/api/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.data[0]['username'] == 'apiuser'

@pytest.mark.django_db
def test_api_me_authenticated():
    User = get_user_model()
    user = User.objects.create_user('apiuser', 'apiuser@test.com', 'Abc12345')
    client = APIClient()
    client.force_authenticate(user=user)
    url = '/dashboard/api/me/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['username'] == 'apiuser'

@pytest.mark.django_db
def test_api_list_unauthenticated():
    client = APIClient()
    url = '/dashboard/api/'
    response = client.get(url)
    assert response.status_code == 401

@pytest.mark.django_db
def test_api_me_unauthenticated():
    client = APIClient()
    url = '/dashboard/api/me/'
    response = client.get(url)
    assert response.status_code == 401
