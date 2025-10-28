from django.db import models



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
    is_published = models.BooleanField(default=False, verbose_name='Publicado?')
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='',)
    
    class Meta:
        verbose_name = "Receita"
        verbose_name_plural = "Receitas"
    def __str__(self):
        return self.title