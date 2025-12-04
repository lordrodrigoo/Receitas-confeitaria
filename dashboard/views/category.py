from django.views import View
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from recipes.models import Category, Recipe
from dashboard.forms import CategoryDeleteForm, EditCategoryForm

def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser, login_url='dashboard:dashboard')(view_func)

@method_decorator([login_required(login_url='dashboard:login'), superuser_required], name='dispatch')
class CategoryDeleteView(View):
    def post(self, request, *args, **kwargs):
        form = CategoryDeleteForm(request.POST)
        if form.is_valid():
            category_id = form.cleaned_data['category_id']
            category = get_object_or_404(Category, id=category_id)
            if Recipe.objects.filter(category=category).exists():
                messages.error(request, 'Não é possível excluir uma categoria que possui receitas.')
            else:
                category.delete()
                messages.success(request, 'Categoria excluída com sucesso!')
        else:
            messages.error(request, 'Requisição inválida para exclusão de categoria.')
        return redirect(reverse('dashboard:dashboard'))

@method_decorator([login_required(login_url='dashboard:login'), superuser_required], name='dispatch')
class CategoryEditView(View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = EditCategoryForm(instance=category)
        return render(request, 'dashboard/pages/edit_category.html', {
            'form': form,
            'category': category,
            'form_action': reverse('dashboard:edit_category', args=[pk]),
        })

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        form = EditCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria editada com sucesso!')
            return redirect('dashboard:dashboard')
        return render(request, 'dashboard/pages/edit_category.html', {
            'form': form,
            'category': category,
            'form_action': reverse('dashboard:edit_category', args=[pk]),
        })
