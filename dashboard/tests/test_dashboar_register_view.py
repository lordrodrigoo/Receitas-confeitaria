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
        