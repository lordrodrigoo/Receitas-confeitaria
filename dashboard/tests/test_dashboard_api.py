import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

class TestAuthorViewSet:
	@pytest.mark.django_db
	def test_list_authenticated(self):
		User = get_user_model()
		user = User.objects.create_user(username='user1', password='testpass')
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.get('/dashboard/api/')
		assert response.status_code == 200
		assert response.data[0]['username'] == 'user1'

	@pytest.mark.django_db
	def test_list_unauthenticated(self):
		client = APIClient()
		response = client.get('/dashboard/api/')
		assert response.status_code == 403 or response.status_code == 401

	@pytest.mark.django_db
	def test_me_authenticated(self):
		User = get_user_model()
		user = User.objects.create_user(username='user2', password='testpass')
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.get('/dashboard/api/me/')
		assert response.status_code == 200
		assert response.data['username'] == 'user2'

	@pytest.mark.django_db
	def test_me_unauthenticated(self):
		client = APIClient()
		response = client.get('/dashboard/api/me/')
		assert response.status_code == 403 or response.status_code == 401
