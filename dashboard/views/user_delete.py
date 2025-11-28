from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from dashboard.forms.user_delete_form import UserDeleteForm

def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser, login_url='dashboard:dashboard')(view_func)

@method_decorator([login_required(login_url='dashboard:login'), superuser_required], name='dispatch')
class UserDeleteView(View):
    def post(self, request, *args, **kwargs):
        form = UserDeleteForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            user = get_object_or_404(User, id=user_id)
            if user.is_superuser:
                messages.error(request, 'Não é possível excluir um superusuário.')
            else:
                user.delete()
                messages.success(request, 'Usuário excluído com sucesso!')
        else:
            messages.error(request, 'Requisição inválida para exclusão de usuário.')
        return redirect(reverse('dashboard:dashboard'))
