import os 

from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from recipes.models import Recipe
from ..serializers import RecipeSerializer
from rest_framework.views import APIView


class RecipeAPIv1Pagination(PageNumberPagination):
    page_size = int(os.environ.get('PER_PAGE', 9))


class RecipeAPIv1ViewSet(ModelViewSet):
    queryset = Recipe.objects.filter(is_published=True).order_by('-id')
    serializer_class = RecipeSerializer
    pagination_class = RecipeAPIv1Pagination


class RecipeListAPIv1(APIView):
    def get(self, request):
        recipes = Recipe.objects.filter(is_published=True).order_by('-id')
        paginator = RecipeAPIv1Pagination()
        paginated_recipes = paginator.paginate_queryset(recipes, request)
        serializer = RecipeSerializer(paginated_recipes, many=True)
        return paginator.get_paginated_response(serializer.data)