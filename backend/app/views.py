from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.app.filters import RecipesFilter
from backend.app.mixin import UpdateDeleteViewSet
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
    queryset = Favorite.objects.all()

    def get_queryset(self):
        print(f'DDDDDDDDDcccccccDDDDDDDDDDDD::::;')
        recipe_id = self.kwargs.get("id")
        new_queryset = Recipes.objects.filter(pk=recipe_id)
        new_queryset.update(is_favorited=1)
        return new_queryset

    # Пишем метод, а в декораторе разрешим работу со списком объектов
    # и переопределим URL на более презентабельный

    @action(methods=['delete'], detail=False,
            url_path='/api/recipes/6/favorite/')
    def del_white_cats(self, request):
        print(f'DDD1222222DDDDD::::;{request}')
        # Нужны только последние пять котиков белого цвета
        cats = Recipes.objects.filter(color='White')[:5]
        # Передадим queryset cats сериализатору
        # и разрешим работу со списком объектов
        serializer = self.get_serializer(cats, many=True)
        return Response(serializer.data)


# def destroy(self, request, *args, **kwargs):
#         print(f'DDDDZZZZZZZZZZZZZZZZZZZDDDDDDDDD::::;')
#         try:
#             instance = self.get_object()
#             self.perform_destroy(instance)
#         except Http404:
#             pass
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @action(methods=['delete'], detail=True, url_path='recipes/(?P<phone_pk>[^/.]+)')
# def delete(self, request):
#     print(f'DDDDDDDDDDDDDDDDDDDDD::::;{request}')
#     try:
#         instance = self.get_object()
#     except Http404:
#         pass
#     return Response(status=status.HTTP_204_NO_CONTENT)

# @action(detail=True,
#         methods=['delete'],
#         url_path='recipes/(?P<phone_pk>[^/.]+)')
# def delete_phone(self, request, phone_pk, pk=None):
#     print(f'DDDDDDDDDDDDDDDDDDDDD::::;{request}')
#
#     contact = self.get_object()
#     phone = get_object_or_404(contact.phone_qs, pk=phone_pk)
#     phone.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCardModelViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        # Получаем id рецепта из эндпоинта
        recipe_id = self.kwargs.get("id")
        # И отбираем только купленные
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

#
# @api_view(['DELETE'])
# def del_favor(request):
#     print(f'DDDDDDDDDDDDDDDDDDDDD::::;{request}')
#     #     try:
#     #         instance = self.get_object()
#     #     except Http404:
#     #         pass
#     #     return Response(status=status.HTTP_204_NO_CONTENT)
