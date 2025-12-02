from .test_dashboard_base import DashboardBaseTest
from django.urls import reverse


class RegisterViewTest(DashboardBaseTest):
        
    
    def test_register_view_returns_status_200(self):
        url = reverse('dashboard:register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_correct_template_used_in_register_view(self):
        url = reverse('dashboard:register')
        response = self.client.get(url)
        self.assertTemplateUsed(
            response,
            'dashboard/pages/register_view.html'
        )

    def test_form_is_passed_in_context(self):
        url = reverse('dashboard:register')
        response = self.client.get(url)
        form = response.context['form']
        self.assertIsNotNone(form)
        self.assertIn('form', response.context)
        
    def test_register_view_form_is_register_form(self):
        url = reverse('dashboard:register')
        response = self.client.get(url)
        from dashboard.forms import RegisterForm
        self.assertIsInstance(response.context['form'], RegisterForm)

    def test_register_view_has_form_action_in_context(self):
        url = reverse('dashboard:register')
        response = self.client.get(url)
        self.assertIn('form_action', response.context)
    
    def test_register_create_get_returns_404(self):
        url = reverse('dashboard:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_login_create_get_returns_404(self):
        url = reverse('dashboard:login_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_login_create_post_invalid_form(self):
        url = reverse('dashboard:login_create')
        data = {'usuario': '', 'senha': ''}
        response = self.client.post(url, data, follow=True)
        messages = list(response.wsgi_request._messages)

        self.assertTrue(any('Nome de usuário ou senha inválidos' in str(m) for m in messages))
        # Verify redirection to login page
        self.assertTemplateUsed(response, 'dashboard/pages/dashboard_login.html')

    def test_login_create_post_invalid_credentials(self):
        url = reverse('dashboard:login_create')
        data = {'usuario': 'usernaoexiste', 'senha': 'senhaerrada'}
        response = self.client.post(url, data, follow=True)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('Credenciais inválidas' in str(m) for m in messages))
        self.assertTemplateUsed(response, 'dashboard/pages/dashboard_login.html')

    def test_login_create_post_valid_credentials(self):
        # Create a valid user first
        user = self.create_user(username='usuario', password='senha123')
        url = reverse('dashboard:login_create')
        data = {'usuario': 'usuario', 'senha': 'senha123'}
        response = self.client.post(url, data)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('Você está logado.' in str(m) for m in messages))
        self.assertRedirects(response, reverse('dashboard:dashboard'))

    def test_register_create_post_valid_data_creates_user_and_redirects(self):
        url = reverse('dashboard:register_create')
        data = {
            'username': 'novousuario',
            'email': 'novo@email.com',
            'first_name': 'João',
            'last_name': 'Silva',
            'password': 'SenhaForte123',
            'ConfirmPassword': 'SenhaForte123',
        }
        response = self.client.post(url, data, follow=True)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.assertTrue(User.objects.filter(username='novousuario').exists())
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('Usuário criado com sucesso' in str(m) for m in messages))
        self.assertTemplateUsed(response, 'dashboard/pages/dashboard_login.html')


    def test_register_create_post_invalid_data_redirects_to_register(self):
        url = reverse('dashboard:register_create')
        data = {
            'username': '',  # invalid username
            'email': 'invalido',
            'password': '123',
            'ConfirmPassword': '456',
        }
        response = self.client.post(url, data, follow=True)
        # Must redirect to the register template
        self.assertTemplateUsed(response, 'dashboard/pages/register_view.html')
        

    def test_add_person_get_as_superuser_renders_form(self):
            superuser = self.create_superuser(username='admin', password='admin123')
            self.login_user(superuser)
            url = reverse('dashboard:add_person')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'dashboard/pages/add_person.html')
            self.assertIn('form', response.context)

    def test_add_person_post_valid_creates_user_and_redirects(self):
        superuser = self.create_superuser(username='admin', password='admin123')
        self.login_user(superuser)
        url = reverse('dashboard:add_person')
        data = {
            'username': 'pessoa',
            'email': 'pessoa@email.com',
            'first_name': 'Pessoa',
            'last_name': 'Teste',
            'password': 'SenhaForte123',
            'ConfirmPassword': 'SenhaForte123',
        }
        response = self.client.post(url, data, follow=True)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.assertTrue(User.objects.filter(username='pessoa').exists())
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('Usuário criado com sucesso' in str(m) for m in messages))
        self.assertTemplateUsed(response, 'dashboard/pages/dashboard.html')

    def test_add_person_post_invalid_shows_form_with_errors(self):
        superuser = self.create_superuser(username='admin', password='admin123')
        self.login_user(superuser)
        url = reverse('dashboard:add_person')
        data = {
            'username': '',  # inválido
            'email': 'invalido',
            'first_name': '',
            'last_name': '',
            'password': '123',
            'ConfirmPassword': '456',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/pages/add_person.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_add_person_get_without_login_redirects(self):
        url = reverse('dashboard:add_person')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard/login/', response.url)

    def test_logout_view_post_valid_logs_out(self):
        user = self.create_user(username='usuario', password='senha123')
        self.login_user(user)
        url = reverse('dashboard:logout')
        data = {'username': user.username}
        response = self.client.post(url, data, follow=True)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('Logout realizado com sucesso.' in str(m) for m in messages))
        self.assertTemplateUsed(response, 'dashboard/pages/dashboard_login.html')

    def test_logout_view_post_invalid_username(self):
        user = self.create_user(username='usuario', password='senha123')
        self.login_user(user)
        url = reverse('dashboard:logout')
        data = {'username': 'outro'}
        response = self.client.post(url, data, follow=True)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('Usuário de logout inválido' in str(m) for m in messages))
        self.assertTemplateUsed(response, 'dashboard/pages/dashboard_login.html')

    def test_logout_view_get_shows_error(self):
        user = self.create_user(username='usuario', password='senha123')
        self.login_user(user)
        url = reverse('dashboard:logout')
        response = self.client.get(url, follow=True)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('Requisição de logout inválida' in str(m) for m in messages))
        self.assertTemplateUsed(response, 'dashboard/pages/dashboard_login.html')
