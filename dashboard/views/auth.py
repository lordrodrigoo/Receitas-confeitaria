from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from dashboard.forms import LoginForm

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
