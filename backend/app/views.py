
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser

from backend.app.filters import RecipesFilter
from .models import Ingredient, Tag, Recipes, User
from .serializers import (IngredientSerializer, TagSerializer,
                          RecipesSerializer)


class IngredientModelViewSet(viewsets.ModelViewSet):
    """Пользовательская модель пользователя с настраиваемым действием."""
    queryset = Ingredient.objects.all().order_by("-id")
    serializer_class = IngredientSerializer


class TagModelViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipesModelViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    parser_classes = (MultiPartParser, JSONParser)
    filterset_class = RecipesFilter

    # def perform_create(self, serializer):
    #     print(f'SVCCCCCCCC:: {self.request.data}')
    #     print(f'USSSSSSSSSSSSSS:::: {self.request.user}')
    #     user = get_object_or_404(User, email=self.request.user)
    #     serializer.save(image=self.request.data['image'],author=user)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # def perform_create(self, serializer):
    #     ingredients = self.request.data["ingredients"]
    #     slug_tag = self.request.data['tags']
    #     print(f'FOOOO: {slug_tag}')
    #     print(f'FOOOO2: {ingredients}')
    #
    #     tag = get_object_or_404(Tag, pk=slug_tag[0])
    #     recipe = serializer.save(tag_id=tag.id)
    #
    #     for ingrd in ingredients:
    #         ingredient = get_object_or_404(Ingredient, pk=ingrd.id)
    #         print(f'goo:: {ingredient}')
    #         recipe.ingredients.add(ingredient)
        # serializer.save(author=self.request.user, review=review, title=title)
        # return Response(serializer.data, status=status.HTTP_200_OK)

    # elif request.method == 'POST':
    #     serializer = RecipesSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=201)
    #     return Response(serializer.errors, status=400)


def index(request):
    return render(request, 'index.html', {})
