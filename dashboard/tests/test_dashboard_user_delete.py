import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from dashboard.forms.user_delete_form import UserDeleteForm

class TestUserDeleteView:
    @pytest.mark.django_db
    def test_delete_user_requires_superuser(self):
        user = User.objects.create_user(username='normal', password='123')
        client = Client()
        client.login(username='normal', password='123')
        user_to_delete = User.objects.create_user(username='delete_me', password='123')
        form = UserDeleteForm({'user_id': user_to_delete.id})
        response = client.post(reverse('dashboard:dashboard_user_delete'), data=form.data)
        expected_url = reverse('dashboard:dashboard') + '?next=' + reverse('dashboard:dashboard_user_delete')
        assert response.status_code == 302
        assert response.url == expected_url

    @pytest.mark.django_db
    def test_delete_superuser_not_allowed(self):
        admin = User.objects.create_superuser(username='admin', password='123')
        client = Client()
        client.login(username='admin', password='123')
        superuser = User.objects.create_superuser(username='super', password='123')
        form = UserDeleteForm({'user_id': superuser.id})
        response = client.post(reverse('dashboard:dashboard_user_delete'), data=form.data, follow=True)
        assert User.objects.filter(id=superuser.id).exists()
        assert 'Não é possível excluir um superusuário.' in response.content.decode()

    @pytest.mark.django_db
    def test_delete_user_success(self):
        admin = User.objects.create_superuser(username='admin', password='123')
        client = Client()
        client.login(username='admin', password='123')
        user_to_delete = User.objects.create_user(username='delete_me', password='123')
        form = UserDeleteForm({'user_id': user_to_delete.id})
        response = client.post(reverse('dashboard:dashboard_user_delete'), data=form.data, follow=True)
        assert not User.objects.filter(id=user_to_delete.id).exists()
        assert 'Usuário excluído com sucesso!' in response.content.decode()

    @pytest.mark.django_db
    def test_delete_user_invalid_form(self):
        admin = User.objects.create_superuser(username='admin', password='123')
        client = Client()
        client.login(username='admin', password='123')
        form = UserDeleteForm({'user_id': ''})
        response = client.post(reverse('dashboard:dashboard_user_delete'), data=form.data, follow=True)
        assert 'Requisição inválida para exclusão de usuário.' in response.content.decode()
