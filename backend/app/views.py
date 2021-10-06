from coreapi.utils import File
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django.shortcuts import render
from foodgram.settings import MEDIA_ROOT, SUB_DIR_RECIPES
from rest_framework import viewsets, generics, renderers
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser, MultiPartParser
from backend.app.filters import RecipesFilter
from .models import Favorite, Ingredient, Recipes, Tag
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipesSerializer, TagSerializer)

User = get_user_model()


class StandardResultsSetPagination(PageNumberPagination):
    # Класс ModelViewSet предоставляет следующие действия: .list ()
    # .retrieve (), .create (), .update (), .partial_update () и .destroy ()
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class IngredientModelViewSet(viewsets.ReadOnlyModelViewSet):
    """Пользовательская модель пользователя с настраиваемым действием."""
    queryset = Ingredient.objects.all().order_by("-id")
    serializer_class = IngredientSerializer
    paginator = None


class TagModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [SearchFilter]
    search_fields = ['tags']
    paginator = None

    # def get_queryset(self):
    #     print(f'self.request.query_params::: {self.request.query_params}')
    #     qs = super().get_queryset()
    #     slug = self.request.query_params.get('slug')
    #     return qs.filter(results__tags__iexact=slug)
    # def list(self, request):
    #     tags_data = Tag.objects.all()
    #
    #     page = self.paginate_queryset(tags_data)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(tags_data, many=True)
    #     return Response(serializer.data)


class FavoriteModelViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

    # def get_queryset(self):
    #     user = get_object_or_404(User, email=self.request.user)
    #     recipe_id = self.kwargs.get("id")
    #     # rc2.is_favorited.add(us[3])
    #
    #     new_queryset = Recipes.objects.filter(pk=recipe_id)
    #     user.favorite_recipe.add(new_queryset)
    #     print(f'FSSSSSSSSS:::{new_queryset}')
    #
    #     # new_queryset.objects.add(self.request.user)
    #     # new_queryset.update(is_favorited=1)
    #     return new_queryset
    #
    # # Пишем метод, а в декораторе разрешим работу со списком объектов
    # # и переопределим URL на более презентабельный
    #
    # @action(methods=['delete'], detail=False,
    #         url_path='/api/recipes/6/favorite/')
    # def del_white_cats(self, request):
    #     print(f'DDD1222222DDDDD::::;{request}')
    #     # Нужны только последние пять котиков белого цвета
    #     cats = Recipes.objects.filter(color='White')[:5]
    #     # Передадим queryset cats сериализатору
    #     # и разрешим работу со списком объектов
    #     serializer = self.get_serializer(cats, many=True)
    #     return Response(serializer.data)


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

    @action(detail=True, methods=['put'])
    def tags(self, request, pk=None):
        user = self.get_object()
        tags = user.tags
        print(f'tags:::::::::::::{tags}')
        serializer = TagSerializer(tags, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    # @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    # def highlight(self, request, *args, **kwargs):
    #     recipes = self.get_object()
    #     return Response(recipes.highlighted)
    #
    # @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    # def download_pdf(request):
    #     path_to_file = MEDIA_ROOT + '/filename.pdf'
    #     f = open(path_to_file, 'rb')
    #     pdf_file = File(f)
    #     response = HttpResponse(pdf_file.read())
    #     response['Content-Disposition'] = 'attachment;'
    #     return response

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@api_view(['GET'])
def download_pdf(request):
    path_to_file = MEDIA_ROOT + '/filename.pdf'
    f = open(path_to_file, 'rb')
    pdf_file = File(f)
    response = HttpResponse(pdf_file.read())
    response['Content-Disposition'] = 'attachment;'
    return response


@api_view(['DELETE'])
def del_favor(request):
    print(f'DDDDDDDDDDDDDDDDDDDDD::::;{request}')
    #     try:
    #         instance = self.get_object()
    #     except Http404:
    #         pass
    #     return Response(status=status.HTTP_204_NO_CONTENT)


def index(request):
    return render(request, 'index.html', {})
