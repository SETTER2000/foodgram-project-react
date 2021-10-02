from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, JSONParser
from backend.app.filters import RecipesFilter
from .models import Ingredient, Tag, Recipes, Favorite
from .serializers import (IngredientSerializer, TagSerializer,
                          RecipesSerializer, FavoriteSerializer)


class IngredientModelViewSet(viewsets.ReadOnlyModelViewSet):
    """Пользовательская модель пользователя с настраиваемым действием."""
    queryset = Ingredient.objects.all().order_by("-id")
    serializer_class = IngredientSerializer


class TagModelViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class FavoriteModelViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer

    def get_queryset(self):

        recipe_id = self.kwargs.get("id")

        new_queryset = Recipes.objects.filter(pk=recipe_id)
        return new_queryset


class RecipesModelViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    # authentication_classes = (TokenAuthentication,)
    parser_classes = (MultiPartParser, JSONParser)
    filterset_class = RecipesFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


def index(request):
    return render(request, 'index.html', {})
