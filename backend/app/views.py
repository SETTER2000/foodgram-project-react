from coreapi.utils import File
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from functools import partial
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.filters import SearchFilter
from rest_framework import filters, permissions, viewsets, renderers, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.utils import json

from backend.app.pagination import PaginationNull, PaginationAll

from foodgram.settings import DEFAULT_FROM_EMAIL, ROLES_PERMISSIONS, ROOT_URLCONF
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
from ..users.serializers import UserSerializer

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
    search_fields = ("slug",)


class FavoriteModelViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    queryset = Recipes.objects.all()
    permission_classes = (
        (IsAuthenticatedOrReadOnly & IsAuthorOrReadOnly)
        | partial(PermissonForRole, ROLES_PERMISSIONS.get("Reviews")),
    )

    def get_queryset(self):
        """Добавит рецепт в избранное."""
        user = get_object_or_404(User, email=self.request.user)
        recipe = Recipes.objects.get(pk=self.kwargs["id"])
        # user = User.objects.get(email=self.request.user)

        if user is None:
            raise ParseError("Неверный запрос!")
        recipe.is_favorited.add(user)
        return self.queryset

    def delete(self, request, id=None):
        """Удалить рецепт из избранного."""
        user = get_object_or_404(User, email=self.request.user)
        recipe = Recipes.objects.get(pk=self.kwargs["id"])
        # user = User.objects.get(email=self.request.user)
        recipe.is_favorited.remove(user)
        recipe.save()
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
    pagination_class = PaginationAll
    permission_classes = [IsAuthorOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, JSONParser)
    filter_backends = (DjangoFilterBackend,)

    # filterset_class = RecipesFilter

    # @action(detail=True, methods=['put'])
    # def tags(self, request, pk=None):
    #     user = self.get_object()
    #     tags = user.tags
    #     print(f'tags:::::::::::::{tags}')
    #     serializer = TagSerializer(tags, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=200)
    #     else:
    #         return Response(serializer.errors, status=400)

    def perform_create(self, serializer):
        user = User.objects.filter(email=self.request.user)
        if not user.exists():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save(author=self.request.user, data=self.request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action == 'list':
            # ...то применяем CatListSerializer
            return RecipesListSerializer
        return RecipesSerializer


# def absolutePosition(self, x, y):
#     return x, y


@api_view(['GET'])
def download_pdf(request):
    pdfmetrics.registerFont(TTFont('abc', 'static/Oswaldlight.ttf'))
    # Создайте файловый буфер для приема данных PDF.
    buffer = io.BytesIO()

    # Создайте объект PDF, используя буфер в качестве «файла».
    c = canvas.Canvas(buffer, pagesize=letter, bottomup=0)

    c.setFillColor(HexColor('#08073b'))
    c.setFont('Courier-Bold', 36)
    c.drawCentredString(300, 100, 'Recipes Shopping')

    c.setFont('Helvetica-Bold', 18)
    c.drawCentredString(300, 750, '© Foodgram')
    c.line(30, 710, 580, 710)
    text_obj = c.beginText()
    text_obj.setTextOrigin(inch + 55, inch + 90)
    text_obj.setFont('abc', 18)
    text_obj.setFillColor(HexColor('#79797e'))

    serializer = UserSerializer(request.user)

    # for font in c.getAvailableFonts():
    #     print(font)

    recipes = Recipes.objects.filter(is_in_shopping_cart__id=serializer.data['id'])
    lines = []
    for recipe in recipes:
        lines.append(f'#{recipe.id}:  {recipe.name} | время приготовления {recipe.cooking_time}')
        lines.append(' ')

    for line in lines:
        text_obj.textLine(line)

    # # перемещаем начало координат вверх и влево
    # c.translate(inch, 750)
    c.drawText(text_obj)

    # выберите цвета
    c.setStrokeColorRGB(0.2, 0.5, 0.3)
    c.setFillColorRGB(1, 0, 1)
    # рисуем прямоугольник
    # c.rect(inch, inch, 6 * inch, 9 * inch, fill=1)
    # заставить текст идти прямо вверх
    # c.rotate(90)
    # change color
    c.setFillColorRGB(0, 0, 0.77)
    # Закройте объект PDF аккуратно, и все готово.
    c.showPage()
    c.save()

    # FileResponse устанавливает заголовок Content-Disposition, чтобы браузеры
    # представить возможность сохранения файла.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='recipes_shopping.pdf')


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
