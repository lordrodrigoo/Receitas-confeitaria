from collections import defaultdict

from django import forms
from recipes.models import Recipe
from django.core.exceptions import ValidationError
from utils.django_forms import add_attr
from dashboard.validators import RecipeDashboardValidator


class DashboardRecipeForm(forms.ModelForm):
    from django.contrib.auth.models import User
    author = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label='Autor',
        required=False,
        widget=forms.Select(),
        help_text='Selecione um autor existente adicione um novo autor.'
    )
    new_author = forms.CharField(
        max_length=150,
        required=False,
        label='Novo autor',
        widget=forms.TextInput(attrs={'placeholder': 'Digite o nome do novo autor (opcional)'}),
        
    )
    new_category = forms.CharField(
    max_length=65,
    required=False,
    label='Nova categoria',
    widget=forms.TextInput(attrs={'placeholder': 'Digite uma nova categoria (opcional)'}),
)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._my_errors = defaultdict(list)
        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        # Preenche o campo author_name com o nome do autor, se houver instance
        if self.instance and self.instance.pk and self.instance.author:
            self.fields['author'].initial = self.instance.author.pk

    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'preparation_time', 'preparation_time_unit',
            'servings', 'servings_unit', 'preparation_steps', 'cover', 'category', 'new_category', 'author', 'new_author'
        ]
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('pessoas', 'Pessoas'),
                    ('pessoa', 'Pessoa'),
                    ('porção', 'Porção'),
                    ('porções', 'Porções'),
                    ('fatia', 'Fatia'),
                    ('fatias', 'Fatias'),
                ),
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('min', 'Minutos'),
                    ('hora', 'Horas'),
                ),
            ),
            'category': forms.Select(),
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category')
        author = cleaned_data.get('author')
        new_author = cleaned_data.get('new_author')
        if not category and not new_category:
            raise ValidationError('Escolha uma categoria existente ou crie uma nova.')
        if not author and not new_author:
            raise ValidationError('Selecione um autor existente ou crie um novo.')
        return cleaned_data