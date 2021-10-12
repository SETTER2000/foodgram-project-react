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
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipesIngredients
        fields = ('id', 'name', 'measurement_unit', 'amount',)

    # def create(self, validated_data):
    #     ingredients_data = validated_data['data'].pop('ingredients')
    #     tags_data = validated_data['data'].pop('tags')
    #     recipe = Recipes.objects.create(**validated_data['data'])
    #     recipe.author = validated_data['author']
    #     recipe.save()
    #     for tag_data in tags_data:
    #         tg = Tag.objects.get(id=tag_data)
    #         tg.recipes.add(recipe)
    #         tg.save()
    #
    #     for ingredient_data in ingredients_data:
    #         ingredient = Ingredient.objects.get(id=ingredient_data["id"])
    #         recipe.ingredients.add(ingredient)
    #         recipe.save()
    #         ri = RecipesIngredients.objects.last()
    #         ri.amount = ingredient_data["amount"]
    #         ri.save()
    #
    #     return recipe


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(required=False)
    measurement_unit = serializers.ReadOnlyField(required=False)

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageFieldToFile()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    ingredients = RecipesIngredientsSerializer(
        source='recipesingredients_set', many=True)

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
        return False

    def get_is_in_shopping_cart(self, obj):
        return False

    def to_representation(self, instance):
        """Добавляет автора рецепта при создании."""
        representation = super().to_representation(instance)
        representation["author"] = AuthorSerializer(instance.author).data
        return representation

    def image_convert(self, img: base64):
        """Конвертирует картинку из base64 в строку."""
        os.makedirs(f'{MEDIA_ROOT}/{SUB_DIR_RECIPES}', exist_ok=True)
        try:
            format, imgstr = img.split(';base64,')
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

    def create(self, validated_data):
        print(f'validated_data::: {validated_data["data"]["image"]}')
        img = validated_data["data"]["image"]
        ingredients_data = validated_data['data'].pop('ingredients')
        tags_data = validated_data['data'].pop('tags')
        validated_data["data"]["image"] = self.image_convert(img)

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
        # ingredients = serializers.SerializerMethodField()
    # groups = serializers.SerializerMethodField()
    # ingredients = RecipesIngredientsSerializer(
    #     source='ingredient_for_recipes',
    #     many=True)
    # tags = serializers.StringRelatedField(many=True, read_only=True)
    # ingredients = RecipesIngredientsSerializer()
    # ingredients = RecipesIngredientsSerializer()
    # ingredients = serializers.SerializerMethodField()
    # author = serializers.StringRelatedField(read_only=True)


class RecipesListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipesIngredientsSerializer(
        source='recipesingredients_set', many=True)
    image = Base64ImageFieldToFile()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

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

    def get_ingredients(self, obj):
        "obj is a Member instance. Returns list of dicts"""
        recipes = RecipesIngredients.objects.filter(ingredient=obj)
        return [
            RecipesIngredientsSerializer(recipe).data for recipe in recipes]

    def get_is_favorited(self, obj):
        """Устанавливает флаг для избранных рецептов."""
        email = self.context["request"].user
        return len(obj.is_favorited.filter(email=email))

    def get_is_in_shopping_cart(self, obj):
        """Устанавливает флаг для купленных рецептов."""
        email = self.context["request"].user
        return len(obj.is_in_shopping_cart.filter(email=email))

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
