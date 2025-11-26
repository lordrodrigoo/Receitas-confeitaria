import os
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission
from recipes.models import Recipe, Category
from ..serializers import RecipeSerializer, CategorySerializer


class RecipeAPIv1Pagination(PageNumberPagination):
	page_size = int(os.environ.get('PER_PAGE', 9))


class IsSuperUserOrStaff(BasePermission):
	def has_permission(self, request, view):
		return bool(
			request.user and (request.user.is_superuser or request.user.is_staff))


class RecipeAPIv1ViewSet(ModelViewSet):
	permission_classes = [IsSuperUserOrStaff]
	queryset = Recipe.objects.filter(is_published=True).order_by('-id')
	serializer_class = RecipeSerializer
	pagination_class = RecipeAPIv1Pagination


class CategoryPainelAPIViewSet(ModelViewSet):
	permission_classes = [IsSuperUserOrStaff]
	queryset = Category.objects.all().order_by('name')
	serializer_class = CategorySerializer
