from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from recipes.models import Recipe
from ..serializers import RecipeSerializer
from .api_private import RecipeAPIv1Pagination


class RecipeListAPIv1(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        recipes = Recipe.objects.filter(is_published=True).order_by('-id')
        paginator = RecipeAPIv1Pagination()
        paginated_recipes = paginator.paginate_queryset(recipes, request)
        serializer = RecipeSerializer(paginated_recipes, many=True)
        return paginator.get_paginated_response(serializer.data)


class CategoryPublicListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        from recipes.models import Category
        from ..serializers import CategorySerializer
        categories = Category.objects.all().order_by('name')
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)