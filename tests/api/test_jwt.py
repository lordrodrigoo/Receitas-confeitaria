import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_obtain_jwt_token_success():
    """POST to token endpoint with valid credentials returns access and refresh."""
    username = 'jwtuser'
    password = 'JwtPass123!'
    User.objects.create_user(username=username, password=password)

    client = APIClient()
    resp = client.post('/recipes/api/token/', {'username': username, 'password': password}, format='json')
    assert resp.status_code == 200, resp.content
    data = resp.json()
    assert 'access' in data and 'refresh' in data


@pytest.mark.django_db
def test_obtain_jwt_token_invalid_credentials():
    """Invalid credentials should not return tokens."""
    username = 'jwtuser2'
    password = 'JwtPass123!'
    User.objects.create_user(username=username, password=password)

    client = APIClient()
    resp = client.post('/recipes/api/token/', {'username': username, 'password': 'wrong'}, format='json')
    assert resp.status_code != 200
    # ensure no tokens returned
    try:
        data = resp.json()
    except Exception:
        data = {}
    assert 'access' not in data and 'refresh' not in data


@pytest.mark.django_db
def test_refresh_jwt_token():
    """Refresh endpoint should return a new access token when given a valid refresh token."""
    username = 'jwtuser3'
    password = 'JwtPass123!'
    User.objects.create_user(username=username, password=password)

    client = APIClient()
    obt = client.post('/recipes/api/token/', {'username': username, 'password': password}, format='json')
    assert obt.status_code == 200
    refresh = obt.json().get('refresh')
    assert refresh

    ref_resp = client.post('/recipes/api/token/refresh/', {'refresh': refresh}, format='json')
    assert ref_resp.status_code == 200
    assert 'access' in ref_resp.json()


@pytest.mark.django_db
def test_verify_jwt_token():
    """Verify endpoint should validate a correct access token and reject invalid ones."""
    username = 'jwtuser4'
    password = 'JwtPass123!'
    User.objects.create_user(username=username, password=password)

    client = APIClient()
    obt = client.post('/recipes/api/token/', {'username': username, 'password': password}, format='json')
    assert obt.status_code == 200
    access = obt.json().get('access')
    assert access

    verify = client.post('/recipes/api/token/verify/', {'token': access}, format='json')
    assert verify.status_code == 200

    # invalid token
    bad = client.post('/recipes/api/token/verify/', {'token': access + 'bad'}, format='json')
    assert bad.status_code != 200
