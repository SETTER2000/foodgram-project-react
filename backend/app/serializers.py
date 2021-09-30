import os, base64, time

from foodgram.settings import MEDIA_ROOT, SUB_DIR_RECIPES
from .models import Ingredient, Tag, Recipes, User, Favorite
from rest_framework import serializers


class Base64ImageFieldToFile(serializers.Field):
    """ Новый тип поля в serializers.py. для преобразования base64 в файл."""

    def to_representation(self, value):
        """Для чтения.
        Снипет, если нужно вернуть Base64:
        value = f'{MEDIA_ROOT}/{value}'
        with open(value, 'rb') as f:
            str_64 = base64.standard_b64encode(f.read())
        value = (('%s' % str_64.decode().strip()))
        b64 = f'data:image/jpeg;base64,{value}'
        """
        return f'/media/{value}'

    def to_internal_value(self, data):
        """Для записи."""

        dir = f'{MEDIA_ROOT}/{SUB_DIR_RECIPES}'
        os.makedirs(dir, exist_ok=True)

        try:
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            img_data = base64.b64decode(imgstr)
            filename = f'{SUB_DIR_RECIPES}/{int(time.time())}.{ext}'
            full_file_path = f'{MEDIA_ROOT}/{filename}'
            f = open(full_file_path, 'wb')
            f.write(img_data)
            f.close()
        except ValueError:
            raise serializers.ValidationError('С картинкой проблемы.')
        return filename


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Favorite


class AuthorSerializer(serializers.ModelSerializer):
    """Вложенная модель пользователя, для контроля полей в выдаче."""
    class Meta:
        fields = ('id', 'username', 'email', 'last_name', 'first_name')
        model = User


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    image = Base64ImageFieldToFile()

    class Meta:
        fields = (
            'id',
            'tags',
            'ingredients',
            'image',
            'name',
            'text',
            'author',
            'is_favorited',
            'is_in_shopping_cart',
            'cooking_time')

        model = Recipes

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["author"] = AuthorSerializer(instance.author).data
        return representation

    def get_ingredients(self, obj):
        response = []
        for _ingredient in obj.ingredients.all():
            print(f'RRRRROO::: {_ingredient}')
            ingredients_profile = IngredientSerializer(_ingredient, context={
                'request': self.context['request']})
            response.append(ingredients_profile.data)
        return response

    def create(self, validated_data):
        return Recipes.objects.create(**validated_data)
