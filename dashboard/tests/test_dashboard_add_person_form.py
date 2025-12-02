import pytest
from django.contrib.auth.models import User
from dashboard.forms.add_person_form import AddPersonForm

class TestAddPersonForm:
    @pytest.mark.django_db
    def test_valid_form_creates_user(self):
        data = {
            'first_name': 'Rodrigo',
            'last_name': 'Silva',
            'username': 'lordrodrigoo',
            'email': 'rodrigo@example.com',
            'password': 'Senha1234',
        }
        form = AddPersonForm(data)
        assert form.is_valid(), form.errors
        user = form.save()
        assert User.objects.filter(username='lordrodrigoo').exists()
        assert user.check_password('Senha1234')

    @pytest.mark.django_db
    def test_duplicate_username(self):
        User.objects.create_user(username='lordrodrigoo', email='rodrigo@example.com', password='Senha1234')
        data = {
            'first_name': 'Rodrigo',
            'last_name': 'Silva',
            'username': 'lordrodrigoo',
            'email': 'rodrigo2@example.com',
            'password': 'Senha1234',
        }
        form = AddPersonForm(data)
        assert not form.is_valid()
        assert 'Um usuário com este nome de usuário já existe.' in str(form.errors['username'])

    @pytest.mark.django_db
    def test_duplicate_email(self):
        User.objects.create_user(username='user1', email='rodrigo@example.com', password='Senha1234')
        data = {
            'first_name': 'Rodrigo',
            'last_name': 'Silva',
            'username': 'user2',
            'email': 'rodrigo@example.com',
            'password': 'Senha1234',
        }
        form = AddPersonForm(data)
        assert not form.is_valid()
        assert 'Já existe um usuário com esse e-mail.' in str(form.errors)

    @pytest.mark.django_db
    def test_password_strength(self):
        data = {
            'first_name': 'Rodrigo',
            'last_name': 'Silva',
            'username': 'user3',
            'email': 'rodrigo3@example.com',
            'password': 'abc',  # Fraca
        }
        form = AddPersonForm(data)
        assert not form.is_valid()
        assert 'A senha deve conter ao menos 8 caracteres' in str(form.errors)

    @pytest.mark.django_db
    def test_save_commit_false(self):
        data = {
            'first_name': 'Rodrigo',
            'last_name': 'Silva',
            'username': 'user4',
            'email': 'rodrigo4@example.com',
            'password': 'Senha1234',
        }
        form = AddPersonForm(data)
        assert form.is_valid(), form.errors
        user = form.save(commit=False)
        assert not User.objects.filter(username='user4').exists()
        user.save()
        assert User.objects.filter(username='user4').exists()
