from rest_framework import viewsets
from .models import Ingredient, Tag, Recipes
from .serializers import (IngredientSerializer, TagSerializer,
                          RecipesSerializer)


class IngredientModelViewSet(viewsets.ModelViewSet):
    """Пользовательская модель пользователя с настраиваемым действием."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagModelViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipesModelViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer

    # elif request.method == 'POST':
    #     serializer = RecipesSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=201)
    #     return Response(serializer.errors, status=400)
