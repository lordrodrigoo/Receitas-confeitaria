from django import forms
from django.contrib.auth.models import User

class UserDeleteForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput)

    def clean_user_id(self):
        user_id = self.cleaned_data['user_id']
        if not User.objects.filter(id=user_id).exists():
            raise forms.ValidationError('Usuário não encontrado.')
        return user_id
