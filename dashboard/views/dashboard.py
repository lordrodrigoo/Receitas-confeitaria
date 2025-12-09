from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe, Category
from django.contrib.auth.models import User
from dashboard.forms import CategoryDeleteForm, UserDeleteForm

@login_required(login_url='dashboard:login', redirect_field_name='next')
def dashboard_view(request):
    recipes = Recipe.objects.select_related('category', 'author').all()
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
