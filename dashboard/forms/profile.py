from django import forms
from django.contrib.auth.models import User
from utils.django_forms import add_placeholder, strong_password

class AddPersonForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Seu nome de usuário')
        add_placeholder(self.fields['email'], 'E-mail')
        add_placeholder(self.fields['first_name'], 'Primeiro nome')
        add_placeholder(self.fields['last_name'], 'Sobrenome')
        add_placeholder(self.fields['password'], 'Senha')

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Senha',
        help_text='A senha deve conter pelo menos 8 caracteres.'
    )

    username = forms.CharField(
        label='Nome de usuário',
        help_text='Pode conter letras, números, espaços e acentos. Máximo 150 caracteres.',
        max_length=150,
        required=True
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Um usuário com este nome de usuário já existe.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe um usuário com esse e-mail.')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        strong_password(password)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class EditPersonForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Nome de usuário'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Primeiro nome'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Sobrenome'

class UserDeleteForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput)

    def clean_user_id(self):
        user_id = self.cleaned_data['user_id']
        if not User.objects.filter(id=user_id).exists():
            raise forms.ValidationError('Usuário não encontrado.')
        return user_id
