from django.db import models
from django.urls import reverse
from PIL import Image
import os
from django.conf import settings
from django.conf import settings
from django.utils.text import slugify
import string
from random import SystemRandom
from collections import defaultdict
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=65)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['name']

class Recipe(models.Model):
    PREPARATION_TIME_UNIT_CHOICES = [
        ('min', 'Minutos'),
        ('h', 'Horas'),
        ('s', 'Segundos'),
    ]

    SERVINGS_UNIT_CHOICES = [
        ('porcao', 'Porções'),
        ('fatia', 'Fatias'),
        ('unidade', 'Unidades'),
        ('pessoa', 'Pessoas'),
    ]
        

    title = models.CharField(max_length=65, verbose_name='Título')
    description = models.CharField(max_length=165, verbose_name='Descrição')
    slug = models.SlugField(unique=True, verbose_name='Slug')
    preparation_time = models.PositiveIntegerField(verbose_name='Tempo de preparo')
    preparation_time_unit = models.CharField(
        max_length=65,
        default='minutos',
        verbose_name='Tempo',
        choices=PREPARATION_TIME_UNIT_CHOICES
    )

    servings = models.PositiveIntegerField(verbose_name='Rendimento')
    servings_unit = models.CharField(
        max_length=65,
        verbose_name='Unidade do rendimento',
        choices=SERVINGS_UNIT_CHOICES, 
        default='porções'
    )
    preparation_steps = models.TextField(verbose_name='Modo de preparo')
    preparation_steps_is_html = models.BooleanField(
        default=False, verbose_name='O modo de preparo está em HTML?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='',)
    
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Categoria',
        default=None,
    )

    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Autor')

    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id,))
    
    @staticmethod
    def resize_image(image, new_width=800):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pillow = Image.open(image_full_path)
        original_width, original_height = image_pillow.size

        if original_width < new_width:
            image_pillow.close()
            return
        
        new_height = round((new_width * original_height) / original_width)

        new_image = image_pillow.resize(
            (new_width, new_height), Image.Resampling.LANCZOS
            
            )
        
        new_image.save(
            image_full_path,
            optimize=True,
            quality=50,
        )

    def save(self, *args, **kwargs):

        if not self.slug:
            if not self.slug:
                rand_letters = ''.join(SystemRandom().choices(
                    string.ascii_letters + string.digits,
                    k=5
                    )
            )
            self.slug = slugify(f'{self.title}-{rand_letters}')
            slug = f'{slugify(self.title)}'

        saved = super().save(*args, **kwargs)

        if self.cover:
            try:
                self.resize_image(self.cover, 840)
            except FileNotFoundError:
                ...
        return saved
    
    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title,
        ).first()
        
        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append('Já existe uma receita com esse título.')
            
        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = "Receita"
        verbose_name_plural = "Receitas"
        ordering = ['-id']

    def __str__(self):
        return self.title
    