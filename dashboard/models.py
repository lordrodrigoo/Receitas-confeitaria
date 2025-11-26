from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard_profile')
    bio = models.TextField(default='', blank=True)

    