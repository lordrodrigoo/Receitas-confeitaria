from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic import TemplateView
from recipes.models import Recipe, Category
from django.views.generic import TemplateView

from django.db.models import Q
from django.http import Http404
from django.utils.translation import gettext as _
from utils.pagination import make_pagination




# Create your views here.
PER_PAGE = 9



class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipes/pages/home.html'
    ordering = ['-id']
    

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE,
        )
        ctx.update(
            {
                'recipes': page_obj,
                'pagination_range': pagination_range,
            }
        )
        return ctx


class RecipeHomeView(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe_detail.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs
    
    def get_context_data(self, *args, **kwargs):
        ctx =  super().get_context_data(*args, **kwargs)
        ctx.update({
            'is_detail_page': True,
            'categories': Category.objects.all(),
        })
        return ctx
    


class RecipeAboutView(TemplateView):
    template_name = 'recipes/pages/about.html'

    

class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()
        
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            )
        )
        return qs
        
    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        ctx.update({
            'page_title': f'Pesquisa por "{search_term}" | ',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })
        return ctx
    

class CategoryListView(TemplateView):
    template_name = 'recipes/pages/category.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx
    
class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_context_data(self, *args, **kwargs):
        ctx =  super().get_context_data(*args, **kwargs)

        category_translation = _('category')

        ctx.update({
            'title': ctx.get("recipes")[0].category.name if ctx.get("recipes") else "Categoria",
            'categories': Category.objects.all(),
        })
        return ctx
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id')
        )
        if not qs:
            raise Http404()

        return qs
