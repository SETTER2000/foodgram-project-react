import base64
import os
import time

from rest_framework import serializers

from foodgram.settings import MEDIA_ROOT, SUB_DIR_RECIPES

from .models import (Favorite, Ingredient, IngredientRecipes, Recipes,
                     Tag, User)


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


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Favorite

    # def perform_create(self, serializer):
    #     # rc2.is_favorited.add(us[3])
    #     """Чтобы передать новое значение для какого-то поля в метод save(),
    #     нужно переопределить метод perform_create().В метод save() в полe
    #     author передадим объект пользователя, отправившего запрос."""
    #     serializer.save(is_favorited=self.request.user)


class AuthorSerializer(serializers.ModelSerializer):
    """Вложенная модель пользователя, для контроля полей в выдаче."""

    class Meta:
        fields = ('id', 'username', 'email', 'last_name', 'first_name')
        model = User


class IngredientSerializer(serializers.ModelSerializer):
    # amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
    #     read_only_fields = ('name','measurement_unit')  # поля только для чтения
    #
    # def perform_create(self, serializer):
    #     """Чтобы передать новое значение для какого-то поля в метод save(),
    #     нужно переопределить метод perform_create().В метод save() в полe
    #     owner передадим объект пользователя, отправившего запрос."""
    #     serializer.save(name=self.request.name,
    #                     measurement_unit=self.request.measurement_unit)

    # def get_amount(self, obj):
    #     return obj.amount


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    # tags = serializers.StringRelatedField(many=True, read_only=True)
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
        read_only_fields = ('author',)  # поля только для чтения

    # def get_is_in_shopping_cart(self, obj):
    #     print(f'SELFF:::: {self}')
    #     print(f'obj:::: {obj.__dict__}')
    #

    def get_is_favorited(self, obj):
        """Устанавливает флаг для избранных рецептов."""
        email = self.context["request"].user
        return len(obj.is_favorited.filter(email=email))

    def get_is_in_shopping_cart(self, obj):
        """Устанавливает флаг для купленных рецептов."""
        email = self.context["request"].user
        return len(obj.is_in_shopping_cart.filter(email=email))

    # def create(self, validated_data):
    #     ingredients = validated_data.pop('ingredients')
    #     instance = super(RecipesSerializer, self).create(validated_data)
    #     for item in ingredients:
    #         instance.ingredients.add(item['id'])
    #     instance.save()
    #     return instance

    # def create(self, validated_data):
    #     ingredients_data = validated_data.pop('ingredients')
    #     recipe = Recipes.objects.create(**validated_data)
    #     for ingredient_data in ingredients_data:
    #         Ingredient.objects.create(recipe=recipe, **ingredient_data)
    #     return recipe

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["author"] = AuthorSerializer(instance.author).data
        return representation

    def perform_create(self, serializer):
        # rc2.is_favorited.add(us[3])
        """Чтобы передать новое значение для какого-то поля в метод save(),
        нужно переопределить метод perform_create().В метод save() в полe
        author передадим объект пользователя, отправившего запрос."""
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    #  def create(self, validated_data):
    #     tracks_data = validated_data.pop('tags')
    #     recipe = Recipes.objects.create(**validated_data)
    #     for track_data in tracks_data:
    #         Tag.objects.create(recipe=recipe, **track_data)
    #     return recipe

    # def create(self, validated_data):
    #     # Если в исходном запросе не было поля ingredients
    #     if 'ingredients' not in self.initial_data:
    #         # То создаём запись о котике без его достижений
    #         recipe = Recipes.objects.create(**validated_data)
    #         return recipe
    #
    #     # Иначе делаем следующее:
    #     # Уберем список ингредиентов из словаря validated_data и сохраним его
    #     ingredients = validated_data.pop('ingredients')
    #
    #     # Создадим новый рецепт пока без ингредиентов, данных нам достаточно
    #     recipe = Recipes.objects.create(**validated_data)
    #
    #     # Для каждого ингредиента из списка ингредиентов
    #     for ingredient in ingredients:
    #         # Создадим новую запись или получим существующий экземпляр из БД
    #         current_ingredient, status = Ingredient.objects.get_or_create(
    #             **ingredient)
    #         # Поместим ссылку на каждый ингредиент во вспомогательную таблицу
    #         # Не забыв указать к какому рецепту он относится
    #         IngredientRecipes.objects.create(
    #             ingredient=current_ingredient, recipe=recipe)
    #     return recipe
