from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from dashboard.forms import AddPersonForm, EditPersonForm, UserDeleteForm

def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser, login_url='dashboard:dashboard')(view_func)

@method_decorator([login_required(login_url='dashboard:login'), superuser_required], name='dispatch')
class AddPersonView(View):
    def get(self, request):
        form = AddPersonForm()
        return render(request, 'dashboard/pages/add_person.html', {
            'form': form,
            'form_action': reverse('dashboard:add_person'),
        })

    def post(self, request):
        form = AddPersonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário criado com sucesso!')
            return redirect('dashboard:dashboard')
        return render(request, 'dashboard/pages/add_person.html', {
            'form': form,
            'form_action': reverse('dashboard:add_person'),
        })

@method_decorator([login_required(login_url='dashboard:login'), superuser_required], name='dispatch')
class EditPersonView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = EditPersonForm(instance=user)
        return render(request, 'dashboard/pages/edit_person.html', {
            'form': form,
            'user': user,
            'form_action': reverse('dashboard:edit_person', args=[pk]),
        })

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = EditPersonForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário editado com sucesso!')
            return redirect('dashboard:dashboard')
        return render(request, 'dashboard/pages/edit_person.html', {
            'form': form,
            'user': user,
            'form_action': reverse('dashboard:edit_person', args=[pk]),
        })

@method_decorator([login_required(login_url='dashboard:login'), superuser_required], name='dispatch')
class UserDeleteView(View):
    def post(self, request):
        form = UserDeleteForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            user = get_object_or_404(User, id=user_id)
            user.delete()
            messages.success(request, 'Usuário excluído com sucesso!')
        else:
            messages.error(request, 'Requisição inválida para exclusão de usuário.')
        return redirect(reverse('dashboard:dashboard'))
