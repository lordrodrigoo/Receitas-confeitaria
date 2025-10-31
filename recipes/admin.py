from django.contrib import admin
from .models import Recipe, Category
from django.db import models

class CategoryAdmin(admin.ModelAdmin):
    ...
    

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at', 'updated_at')
    list_display_links = ['title', 'created_at']
    search_fields = ['id', 'title', 'description', 'slug', 'preparation_steps']
    list_filter = ['preparation_steps_is_html', 'is_published']
    list_per_page = 10
    list_editable = ['is_published']
    ordering = ['-id']
    prepopulated_fields = {
        'slug': ('title',)
    }


admin.site.register(Category, CategoryAdmin)