from collections import defaultdict

from django import forms
from recipes.models import Recipe
from django.core.exceptions import ValidationError
from utils.django_forms import add_attr
from dashboard.validators import RecipeDashboardValidator


class DashboardRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time',\
        'preparation_time_unit', 'servings', 'servings_unit',\
        'preparation_steps', 'cover'

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
        }
    
    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        RecipeDashboardValidator(self.cleaned_data, ErrorClass=ValidationError)
        return super_clean