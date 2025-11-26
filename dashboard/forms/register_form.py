from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_password



class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Seu username')
        add_placeholder(self.fields['email'], 'Seu e-mail')
        add_placeholder(self.fields['first_name'], 'Ex.: João')
        add_placeholder(self.fields['last_name'], 'Ex.: Silva')
        add_placeholder(self.fields['password'], 'Digite sua senha')
        add_placeholder(self.fields['ConfirmPassword'], 'Confirme sua senha')

    username = forms.CharField(
        label='Username',
        help_text=(
            'Username deve conter entre 4 e 150 caracteres. '
            'Letras, números e @/./+/-/_ apenas.'
        ),
        error_messages={
            'required': 'Este campo não pode ficar vazio',
            'min_length': 'Username deve conter pelo menos 4 caracteres',
            'max_length': 'Username deve conter menos de 150 caracteres',
        },
        min_length=4, max_length=150
    )

    first_name = forms.CharField(
        error_messages={'required': 'Digite seu primeiro nome'},
        label='First name'
    )
    last_name = forms.CharField(
        error_messages={'required': 'Digite seu sobrenome'},
        label='Last name'
    )

    email = forms.EmailField(
        error_messages={'required': 'Digite seu e-mail'},
        label='E-mail',
        help_text='O e-mail deve ser válido.'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'A senha não pode ficar vazia'
        },
        help_text=(
            'A senha deve conter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número. O comprimento deve ser '
            'pelo menos 8 caracteres.'
        ),
        validators=[strong_password],
        label='Password'
    )
    ConfirmPassword = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirmar senha',
        error_messages={
            'required': 'Confirme sua senha'
        },
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError('O e-mail do usuário já está em uso', code='invalid',)

        return email



    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        ConfirmPassword = cleaned_data.get('ConfirmPassword')

        if password != ConfirmPassword:
            password_confirmation_error = ValidationError(
                'As senhas devem ser iguais',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'ConfirmPassword': [password_confirmation_error],
            })