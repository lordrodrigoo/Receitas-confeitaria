from django.views import View
from recipes.models import Recipe
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.contrib import messages
from dashboard.forms.recipe_form import DashboardRecipeForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(
    login_required(
        login_url='dashboard:login',redirect_field_name='next'),
        name='dispatch'
)
class DashboardRecipe(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_recipe(self, id=None):
        recipe = None
        if id is not None:
            recipe = Recipe.objects.filter(
                is_published=False,
                author=self.request.user,
                id = id,
            ).first()

            if not recipe:
                raise Http404()
        return recipe
    

    def render_recipe(self, form):
        return render(
            self.request,
            'dashboard/pages/dashboard_recipe.html',
            context={
                'form': form
            }
        )

    
    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        form = DashboardRecipeForm(instance=recipe)
        return self.render_recipe(form)
    
    def post(self, request, id=None):
        recipe = self.get_recipe(id)
        form = DashboardRecipeForm(
            data = request.POST or None,
            files = request.FILES or None,
            instance = recipe
        )

        if form.is_valid():
            # Now, the form is valid and i can try save it .
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()
            messages.success(request, 'Sua receita foi salva com sucesso.')
            return redirect(reverse('authors:dashboard_recipe_edit', args=(recipe.id,)))

        return self.render_recipe(form)
    
@method_decorator(
    login_required(
        login_url='dashboard:login',redirect_field_name='next'),
        name='dispatch'
)
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))
        recipe.delete()
        messages.success(self.request, 'Sua receita foi deletada com sucesso.')
        return redirect(reverse('dashboard:dashboard'))
