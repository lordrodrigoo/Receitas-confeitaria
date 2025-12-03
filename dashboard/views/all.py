from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from recipes.models import Recipe, Category
from dashboard.forms import RegisterForm, LoginForm
from dashboard.forms.add_person_form import AddPersonForm

from dashboard.forms.category_delete_form import CategoryDeleteForm
from dashboard.forms.user_delete_form import UserDeleteForm
from django.contrib.auth.models import User

def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)  # Bound Form 
    return render(request, 'dashboard/pages/register_view.html', {
        'form': form,
        'form_action': reverse('dashboard:register_create')
    })

def register_create(request):
    if not request.POST:
        raise Http404()
    
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        raw_password = form.cleaned_data['password']
        user.set_password(raw_password)
        user.is_staff = True  # confirm as staff user
        user.save()
        
        messages.success(request, 'Usuário criado com sucesso, faça login.')

        del(request.session['register_form_data'])
        return redirect(reverse('dashboard:login'))

    return redirect('dashboard:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'dashboard/pages/dashboard_login.html', {
        'form': form,
        'form_action': reverse('dashboard:login_create')
    })

def login_create(request):
    if not request.POST:
        raise Http404()
    form = LoginForm(request.POST)

    if form.is_valid():
        usuario = form.cleaned_data.get('usuario', '')
        senha = form.cleaned_data.get('senha', '')
        authenticated_user = authenticate(
            username=usuario,
            password=senha,
        )
        
        if authenticated_user is not None:
            messages.success(request, 'Você está logado.')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Credenciais inválidas')
    else:
        messages.error(request, 'Nome de usuário ou senha inválidos')
    return redirect(reverse('dashboard:dashboard'))

# Decorator for  superuser
def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser, login_url='dashboard:dashboard')(view_func)

@login_required(login_url='dashboard:login', redirect_field_name='next')
@superuser_required
def add_person(request):
    if request.method == 'POST':
        form = AddPersonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('dashboard:dashboard')
    else:
        form = AddPersonForm()
    return render(request, 'dashboard/pages/add_person.html', {
        'form': form,
        'form_action': reverse('dashboard:add_person'),
    })

@login_required(login_url='dashboard:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Requisição de logout inválida')
        return redirect(reverse('dashboard:login'))
    
    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Usuário de logout inválido')
        return redirect(reverse('dashboard:login')) 

    messages.success(request, 'Logout realizado com sucesso.')
    logout(request)
    return redirect(reverse('dashboard:login'))

@login_required(login_url='dashboard:login', redirect_field_name='next')
def dashboard(request):
    # Mostra todas as receitas cadastradas, independente do autor
    recipes = Recipe.objects.all()
    categories = Category.objects.all()
    
    users = User.objects.filter(is_superuser=False)
    category_delete_form = CategoryDeleteForm()
    user_delete_form = UserDeleteForm()
    return render(
        request,
        'dashboard/pages/dashboard.html',
        context={
            'recipes': recipes,
            'categories': categories,
            'category_delete_form': category_delete_form,
            'users': users,
            'user_delete_form': user_delete_form,
        }
    )

