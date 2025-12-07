import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

@pytest.mark.django_db
def test_login_view_get(client):
    url = reverse('dashboard:login')
    response = client.get(url)
    assert response.status_code == 200
    assert 'form' in response.context
    assert 'form_action' in response.context

@pytest.mark.django_db
def test_login_create_post_valid(client, django_user_model):
    user = django_user_model.objects.create_user('usuario', 'usuario@test.com', 'Abc12345')
    url = reverse('dashboard:login_create')
    data = {'usuario': 'usuario', 'senha': 'Abc12345'}
    response = client.post(url, data, follow=True)
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert any('Você está logado.' in m for m in messages)
    assert response.redirect_chain[-1][0].endswith(reverse('dashboard:dashboard'))

@pytest.mark.django_db
def test_login_create_post_invalid_user(client):
    url = reverse('dashboard:login_create')
    data = {'usuario': 'invalido', 'senha': 'Abc12345'}
    response = client.post(url, data, follow=True)
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert any('Credenciais inválidas' in m for m in messages)
    assert response.redirect_chain[-1][0].endswith(reverse('dashboard:dashboard'))

@pytest.mark.django_db
def test_login_create_post_invalid_form(client):
    url = reverse('dashboard:login_create')
    data = {'usuario': '', 'senha': ''}
    response = client.post(url, data, follow=True)
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert any('Nome de usuário ou senha inválidos' in m for m in messages)
    assert response.redirect_chain[-1][0].endswith(reverse('dashboard:dashboard'))

@pytest.mark.django_db
def test_login_create_get_raises_404(client):
    url = reverse('dashboard:login_create')
    response = client.get(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_logout_view_post_valid(client, django_user_model):
    user = django_user_model.objects.create_user('usuario', 'usuario@test.com', 'Abc12345')
    client.force_login(user)
    url = reverse('dashboard:logout')
    data = {'username': 'usuario'}
    response = client.post(url, data, follow=True)
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert any('Logout realizado com sucesso.' in m for m in messages)
    assert response.redirect_chain[-1][0].endswith(reverse('dashboard:login'))

@pytest.mark.django_db
def test_logout_view_post_invalid_request(client, django_user_model):
    user = django_user_model.objects.create_user('usuario', 'usuario@test.com', 'Abc12345')
    client.force_login(user)
    url = reverse('dashboard:logout')
    response = client.get(url, follow=True)
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert any('Requisição de logout inválida' in m for m in messages)
    assert response.redirect_chain[-1][0].endswith(reverse('dashboard:login'))

@pytest.mark.django_db
def test_logout_view_post_invalid_user(client, django_user_model):
    user = django_user_model.objects.create_user('usuario', 'usuario@test.com', 'Abc12345')
    client.force_login(user)
    url = reverse('dashboard:logout')
    data = {'username': 'outro'}
    response = client.post(url, data, follow=True)
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert any('Usuário de logout inválido' in m for m in messages)
    assert response.redirect_chain[-1][0].endswith(reverse('dashboard:login'))
