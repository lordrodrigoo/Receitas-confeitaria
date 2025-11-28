from django import forms
from recipes.models import Recipe, Category

class RecipeForm(forms.ModelForm):
    new_category = forms.CharField(
        max_length=65,
        required=False,
        label='Nova categoria',
        widget=forms.TextInput(attrs={'placeholder': 'Digite uma nova categoria (opcional)'}),
    )

    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'slug', 'preparation_time', 'preparation_time_unit',
            'servings', 'servings_unit', 'preparation_steps', 'preparation_steps_is_html',
            'cover', 'category', 'new_category'
        ]
        widgets = {
            'category': forms.Select(),
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category')
        if not category and not new_category:
            raise forms.ValidationError('Escolha uma categoria existente ou crie uma nova.')
        return cleaned_data
