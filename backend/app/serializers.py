import base64
import os
import time

from rest_framework import serializers

from foodgram.settings import MEDIA_ROOT, SUB_DIR_RECIPES

from .models import (Favorite, Ingredient, Recipes,
                     Tag, User, RecipesIngredients)


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

        os.makedirs(f'{MEDIA_ROOT}/{SUB_DIR_RECIPES}', exist_ok=True)

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


class ShoppingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Favorite


class AuthorSerializer(serializers.ModelSerializer):
    """Вложенная модель пользователя, для контроля полей в выдаче."""

    class Meta:
        fields = ('id', 'username', 'email', 'last_name', 'first_name')
        model = User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipesIngredientsSerializer(serializers.ModelSerializer):
    """Связующая модель имеющая дополнительное поле (боль всего проекта)."""

    class Meta:
        model = RecipesIngredients
        fields = ('amount',)

    # Перенести часть реализации create в класс RecipesSerializer
    # здесь оставить всё что касается create amount
    # сейчас весь рецепт создаётся в этом сериалайзере из-за этого выпадает
    # обработка кртинок
    def create(self, validated_data):
        ingredients_data = validated_data['data'].pop('ingredients')
        tags_data = validated_data['data'].pop('tags')
        recipe = Recipes.objects.create(**validated_data['data'])
        recipe.author = validated_data['author']
        recipe.save()
        for tag_data in tags_data:
            tg = Tag.objects.get(id=tag_data)
            tg.recipes.add(recipe)
            tg.save()

        for ingredient_data in ingredients_data:
            ingredient = Ingredient.objects.get(id=ingredient_data["id"])
            recipe.ingredients.add(ingredient)
            recipe.save()
            ri = RecipesIngredients.objects.last()
            ri.amount = ingredient_data["amount"]
            ri.save()

        return recipe


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    # ingredients = RecipesIngredientsSerializer(
    #     source='ingredient_for_recipes',
    #     many=True)
    # tags = serializers.StringRelatedField(many=True, read_only=True)
    # ingredients = RecipesIngredientsSerializer()
    # ingredients = RecipesIngredientsSerializer()
    # ingredients = serializers.SerializerMethodField()
    # author = serializers.StringRelatedField(read_only=True)
    image = Base64ImageFieldToFile()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    # is_in_shopping_cart = serializers.SerializerMethodField()
    # is_favorited = serializers.ChoiceField(choices=CHOICES)
    # ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipes
        fields = (
            'id',
            'name',
            'tags',
            'ingredients',
            'image',
            'text',
            'author',
            'is_favorited',
            'is_in_shopping_cart',
            'cooking_time')
        read_only_fields = ('author',)

    def get_is_favorited(self, obj):
        """Устанавливает флаг для избранных рецептов."""
        email = self.context["request"].user
        return len(obj.is_favorited.filter(email=email))

    def get_is_in_shopping_cart(self, obj):
        """Устанавливает флаг для купленных рецептов."""
        email = self.context["request"].user
        return len(obj.is_in_shopping_cart.filter(email=email))

    def to_representation(self, instance):
        """Добавляет автора рецепта при создании."""
        representation = super().to_representation(instance)
        representation["author"] = AuthorSerializer(instance.author).data
        return representation

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
