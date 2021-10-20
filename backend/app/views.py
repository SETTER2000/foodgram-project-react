import io
from functools import partial

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ParseError
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from backend.app.pagination import PaginationAll, PaginationNull
from foodgram.settings import DEFAULT_FROM_EMAIL, FONT_PDF, ROLES_PERMISSIONS

from ..users.serializers import UserSerializer
from .models import Ingredient, Recipes, Tag
from .permissions import IsAuthorOrReadOnly, PermissonForRole
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipesListSerializer, RecipesSerializer,
                          TagSerializer)

User = get_user_model()


class IngredientModelViewSet(viewsets.ReadOnlyModelViewSet):
    """Пользовательская модель пользователя с настраиваемым действием."""
    queryset = Ingredient.objects.all().order_by('-id')
    serializer_class = IngredientSerializer
    pagination_class = PaginationNull


class TagModelViewSet(viewsets.ReadOnlyModelViewSet):
    """Теги рецепта."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = PaginationNull
    permission_classes = (
        partial(PermissonForRole, ROLES_PERMISSIONS.get('Tag')),
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug',)


class FavoriteModelViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    queryset = Recipes.objects.all()
    permission_classes = (
        (IsAuthenticatedOrReadOnly & IsAuthorOrReadOnly)
        | partial(PermissonForRole, ROLES_PERMISSIONS.get('Reviews')),
    )

    def get_queryset(self):
        """Добавит рецепт в избранное."""
        user = get_object_or_404(User, email=self.request.user)
        recipe = Recipes.objects.get(pk=self.kwargs['id'])

        if user is None:
            raise ParseError('Неверный запрос!')
        recipe.is_favorited.add(user)
        return self.queryset

    def delete(self, request, id=None):
        """Удалить рецепт из избранного."""
        user = get_object_or_404(User, email=self.request.user)
        recipe = Recipes.objects.get(pk=self.kwargs['id'])
        recipe.is_favorited.remove(user)
        recipe.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCardModelViewSet(viewsets.ModelViewSet):
    serializer_class = RecipesSerializer
    queryset = Recipes.objects.all()
    pagination_class = PaginationAll

    # permission_classes = (
    #     (IsAuthenticatedOrReadOnly & IsAuthorOrReadOnly)
    #     | partial(PermissonForRole, ROLES_PERMISSIONS.get('Shopping')),
    # )

    def get_queryset(self):
        """Добавит рецепт в покупки."""
        try:
            recipe = Recipes.objects.get(pk=self.kwargs['id'])
        except Recipes.DoesNotExist:
            raise Http404('Not found.')
        user = User.objects.get(email=self.request.user)

        if user is None:
            raise ParseError('Неверный запрос!')
        recipe.is_in_shopping_cart.add(user)
        return self.queryset

    @action(
        detail=True,
        methods=['delete'],
        url_path=r'recipes/<int:id>/shopping_cart',
        name='Delete Shopping')
    def delete(self, request, id=None):
        """Удалить рецепт из покупок."""
        recipe = Recipes.objects.get(pk=self.kwargs['id'])
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

    def perform_create(self, serializer):
        user = User.objects.filter(email=self.request.user)
        if not user.exists():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.save(author=self.request.user, data=self.request.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipesListSerializer
        return RecipesSerializer


@api_view(['GET'])
def download_pdf(request):
    get_object_or_404(User, email=request.user)
    serializer = UserSerializer(request.user)
    pdfmetrics.registerFont(TTFont('abc', FONT_PDF))
    buffer = io.BytesIO()

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

    recipes = Recipes.objects.filter(
        is_in_shopping_cart__id=serializer.data['id'])
    lines = []
    for recipe in recipes:
        lines.append(f'#{recipe.id}:  {recipe.name} | '
                     f'время приготовления {recipe.cooking_time}')
        lines.append(' ')

    for line in lines:
        text_obj.textLine(line)

    c.drawText(text_obj)
    c.setStrokeColorRGB(0.2, 0.5, 0.3)
    c.setFillColorRGB(1, 0, 1)
    c.setFillColorRGB(0, 0, 0.77)
    c.showPage()
    c.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True,
                        filename='recipes_shopping.pdf')


@api_view(['POST'])
def email_auth(request):
    """Check email and send to it confirmation code for token auth."""
    user = get_object_or_404(User, email=request.data['email'])
    confirmation_code = get_random_string()
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        subject='Код для генерации токена аутентификации YAMDB',
        message=str(confirmation_code),
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=(request.data['email'],))
    return Response(
        data='Письмо с кодом для аутентификации',
        status=status.HTTP_201_CREATED)
