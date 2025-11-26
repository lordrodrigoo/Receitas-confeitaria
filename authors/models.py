from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Autor')
    bio = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    def __str__(self):
        return f'Perfil de {self.author.username}'

    
