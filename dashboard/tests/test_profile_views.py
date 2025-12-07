import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from dashboard.forms import AddPersonForm, EditPersonForm, UserDeleteForm

@pytest.mark.django_db
def test_add_person_get(client, django_user_model):
    superuser = django_user_model.objects.create_superuser('admin', 'admin@test.com', '123')
    client.force_login(superuser)
    url = reverse('dashboard:add_person')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddPersonForm)

@pytest.mark.django_db
def test_add_person_post_valid(client, django_user_model):
    superuser = django_user_model.objects.create_superuser('admin', 'admin@test.com', '123')
    client.force_login(superuser)
    url = reverse('dashboard:add_person')
    data = {
        'username': 'newuser',
        'email': 'newuser@test.com',
        'first_name': 'Novo',
        'last_name': 'Usuário',
        'password': 'Abc12345',
    }
    response = client.post(url, data, follow=True)
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert any('Usuário criado com sucesso!' in m for m in messages)
    assert User.objects.filter(username='newuser').exists()

@pytest.mark.django_db
def test_add_person_post_invalid(client, django_user_model):
    superuser = django_user_model.objects.create_superuser('admin', 'admin@test.com', '123')
    client.force_login(superuser)
    url = reverse('dashboard:add_person')
    data = {'username': '', 'email': 'invalid', 'password1': 'abc', 'password2': 'xyz'}
    response = client.post(url, data)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddPersonForm)
    assert response.context['form'].errors

@pytest.mark.django_db
def test_edit_person_get(client, django_user_model):
    superuser = django_user_model.objects.create_superuser('admin', 'admin@test.com', '123')
    user = django_user_model.objects.create_user('editme', 'editme@test.com', '123')
    client.force_login(superuser)
    url = reverse('dashboard:edit_person', args=[user.pk])
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], EditPersonForm)
    assert response.context['user'] == user

@pytest.mark.django_db
def test_edit_person_post_valid(client, django_user_model):
    superuser = django_user_model.objects.create_superuser('admin', 'admin@test.com', '123')
    user = django_user_model.objects.create_user('editme', 'editme@test.com', '123')
    client.force_login(superuser)
    url = reverse('dashboard:edit_person', args=[user.pk])
    data = {'username': 'editme', 'email': 'editado@test.com'}
    response = client.post(url, data, follow=True)
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert any('Usuário editado com sucesso!' in m for m in messages)
    user.refresh_from_db()
    assert user.email == 'editado@test.com'

@pytest.mark.django_db
def test_edit_person_post_invalid(client, django_user_model):
    superuser = django_user_model.objects.create_superuser('admin', 'admin@test.com', '123')
    user = django_user_model.objects.create_user('editme', 'editme@test.com', '123')
    client.force_login(superuser)
    url = reverse('dashboard:edit_person', args=[user.pk])
    data = {'username': '', 'email': ''}
    response = client.post(url, data)
    assert response.status_code == 200
    assert isinstance(response.context['form'], EditPersonForm)
    assert response.context['form'].errors

@pytest.mark.django_db
def test_user_delete_post_valid(client, django_user_model):
    superuser = django_user_model.objects.create_superuser('admin', 'admin@test.com', '123')
    user = django_user_model.objects.create_user('delme', 'delme@test.com', '123')
    client.force_login(superuser)
    url = reverse('dashboard:dashboard_user_delete')
    data = {'user_id': user.pk}
    response = client.post(url, data, follow=True)
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert any('Usuário excluído com sucesso!' in m for m in messages)
    assert not User.objects.filter(pk=user.pk).exists()

@pytest.mark.django_db
def test_user_delete_post_invalid(client, django_user_model):
    superuser = django_user_model.objects.create_superuser('admin', 'admin@test.com', '123')
    client.force_login(superuser)
    url = reverse('dashboard:dashboard_user_delete')
    data = {'user_id': ''}
    response = client.post(url, data, follow=True)
    messages = [m.message for m in get_messages(response.wsgi_request)]
    assert any('Requisição inválida para exclusão de usuário.' in m for m in messages)
