from coreapi.utils import File
from functools import partial
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.filters import SearchFilter
from rest_framework import filters, permissions, viewsets, renderers, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from foodgram.settings import DEFAULT_FROM_EMAIL, ROLES_PERMISSIONS
from rest_framework.response import Response
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.utils.crypto import get_random_string
from foodgram.settings import MEDIA_ROOT, SUB_DIR_RECIPES
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser, MultiPartParser
from backend.app.filters import RecipesFilter
from .models import Favorite, Ingredient, Recipes, Tag
from .permissions import IsAuthorOrReadOnly, PermissonForRole
from .serializers import (FavoriteSerializer, ShoppingSerializer,
                          IngredientSerializer,
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
    permission_classes = (
        partial(PermissonForRole, ROLES_PERMISSIONS.get("Tag")),
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
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
    queryset = Recipes.objects.all()
    permission_classes = (
        (IsAuthenticatedOrReadOnly & IsAuthorOrReadOnly)
        | partial(PermissonForRole, ROLES_PERMISSIONS.get("Reviews")),
    )

    def get_queryset(self):
        """Добавит рецепт в избранное."""
        recipe = Recipes.objects.get(pk=self.kwargs["id"])
        user = User.objects.get(email=self.request.user)

        if user is None:
            raise ParseError("Неверный запрос!")
        recipe.is_favorited.add(user)
        return self.queryset

    def delete(self, request, id=None):
        """Удалить рецепт из избранного."""
        recipe = Recipes.objects.get(pk=self.kwargs["id"])
        user = User.objects.get(email=self.request.user)
        recipe.is_favorited.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCardModelViewSet(viewsets.ModelViewSet):
    serializer_class = RecipesSerializer
    queryset = Recipes.objects.all()

    # permission_classes = (
    #     (IsAuthenticatedOrReadOnly & IsAuthorOrReadOnly)
    #     | partial(PermissonForRole, ROLES_PERMISSIONS.get("Shopping")),
    # )

    def get_queryset(self):
        """Добавит рецепт в покупки."""
        recipe = Recipes.objects.get(pk=self.kwargs["id"])
        user = User.objects.get(email=self.request.user)

        if user is None:
            raise ParseError("Неверный запрос!")
        recipe.is_in_shopping_cart.add(user)
        return self.queryset

    @action(
        detail=True,
        methods=['delete'],
        # permission_classes=[IsAuthorOrReadOnly],
        url_path=r'recipes/<int:id>/shopping_cart',
        name='Delete Shopping')
    def delete(self, request, id=None):
        """Удалить рецепт из покупок."""
        recipe = Recipes.objects.get(pk=self.kwargs["id"])
        user = User.objects.get(email=self.request.user)
        recipe.is_in_shopping_cart.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipesModelViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    # authentication_classes = (TokenAuthentication,)
    # parser_classes = (MultiPartParser, JSONParser)
    filter_backends = (DjangoFilterBackend,)
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


@api_view(["POST"])
def email_auth(request):
    """Check email and send to it confirmation code for token auth."""
    user = get_object_or_404(User, email=request.data["email"])
    confirmation_code = get_random_string()
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        subject="Код для генерации токена аутентификации YAMDB",
        message=str(confirmation_code),
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=(request.data["email"],),
    )
    return Response(
        data="Письмо с кодом для аутентификации",
        status=status.HTTP_201_CREATED,
    )


def index(request):
    return render(request, 'index.html', {})
