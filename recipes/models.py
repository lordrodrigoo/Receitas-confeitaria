from django.db import models

# Create your models here.


class Recipe(models.Model):
    title = models.CharField(max_length=65, verbose_name='Título')
    description = models.CharField(max_length=165, verbose_name='Descrição')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    preparation_time = models.PositiveIntegerField(verbose_name='Tempo de preparo')
    preparation_time_unit = models.CharField(
        max_length=65, default='minutos', verbose_name='Unidade do tempo de preparo')
    servings = models.PositiveIntegerField(verbose_name='Rendimento')
    servings_unit = models.CharField(
        max_length=65, verbose_name='Unidade do rendimento')
    preparation_steps = models.TextField(verbose_name='Modo de preparo')
    preparation_steps_is_html = models.BooleanField(
        default=False, verbose_name='O modo de preparo está em HTML?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    is_published = models.BooleanField(default=False, verbose_name='Publicado?')
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='',)
    