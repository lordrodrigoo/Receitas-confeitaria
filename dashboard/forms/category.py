from django import forms
from recipes.models import Category

class CategoryDeleteForm(forms.Form):
    category_id = forms.IntegerField(widget=forms.HiddenInput)

    def clean_category_id(self):
        category_id = self.cleaned_data['category_id']
        if not Category.objects.filter(id=category_id).exists():
            raise forms.ValidationError('Categoria não encontrada.')
        return category_id

class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nome da categoria'})
        }
