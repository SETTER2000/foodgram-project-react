from coreapi.utils import File
from functools import partial
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.filters import SearchFilter
from rest_framework import filters, permissions, viewsets, renderers, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from backend.app.pagination import PaginationNull, PaginationAll

from foodgram.settings import DEFAULT_FROM_EMAIL, ROLES_PERMISSIONS
from rest_framework.response import Response
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.utils.crypto import get_random_string
from foodgram.settings import MEDIA_ROOT, SUB_DIR_RECIPES
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
# from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser, MultiPartParser
from backend.app.filters import RecipesFilter
from .models import Favorite, Ingredient, Recipes, Tag
from .permissions import IsAuthorOrReadOnly, PermissonForRole
from .serializers import (FavoriteSerializer, ShoppingSerializer,
                          IngredientSerializer,
                          RecipesSerializer, TagSerializer,
                          RecipesIngredientsSerializer, RecipesListSerializer)

User = get_user_model()


# class StandardResultsSetPagination(PageNumberPagination):
#     # Класс ModelViewSet предоставляет следующие действия: .list ()
#     # .retrieve (), .create (), .update (), .partial_update () и .destroy ()
#     page_size = 100
#     page_size_query_param = 'page_size'
#     max_page_size = 1000


class IngredientModelViewSet(viewsets.ReadOnlyModelViewSet):
    """Пользовательская модель пользователя с настраиваемым действием."""
    pagination_class = PaginationNull
    queryset = Ingredient.objects.all().order_by("-id")
    serializer_class = IngredientSerializer


class TagModelViewSet(viewsets.ReadOnlyModelViewSet):
    """Теги рецепта."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = PaginationNull
    permission_classes = (
        partial(PermissonForRole, ROLES_PERMISSIONS.get("Tag")),
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"


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
    pagination_class = PaginationAll
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
    # pagination_class = PaginationAll

    # authentication_classes = (TokenAuthentication,)
    parser_classes = (MultiPartParser, JSONParser)
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = RecipesFilter

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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, data=self.request.data)

    def get_serializer_class(self):
        if self.action == 'list':
            # ...то применяем CatListSerializer
            return RecipesListSerializer
        # А если запрошенное действие — не 'list', применяем CatSerializer
        return RecipesSerializer

@api_view(['GET'])
def download_pdf(request):
    path_to_file = MEDIA_ROOT + '/filename.pdf'
    f = open(path_to_file, 'rb')
    pdf_file = File(f)
    response = HttpResponse(pdf_file.read())
    response['Content-Disposition'] = 'attachment;'
    return response


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
