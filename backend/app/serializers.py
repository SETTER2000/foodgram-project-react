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


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipesIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipesIngredients
        fields = ('amount',)

    def create(self, validated_data):
        ingredients_data = validated_data['data'].pop('ingredients')
        tags_data = validated_data['data'].pop('tags')
        # return ingredients_data
        print(f'FFFF-6666:::::::: {ingredients_data}')
        recipe = Recipes.objects.create(**validated_data['data'])
        print(f'FFFFF-555:::::::: {recipe}')
        for tag_data in tags_data:
            tg = Tag.objects.get(id=tag_data)
            tg.recipes.add(recipe)
            tg.save()
        # починить!!!
        for ingredient_data in ingredients_data:
            RecipesIngredients.objects.create(recipe=recipe, **ingredient_data)

        return recipe


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipesSerializer(serializers.ModelSerializer):
    # tags = TagSerializer(many=True, read_only=True)
    # ingredients = RecipesIngredientsSerializer(
    #     source='ingredient_for_recipes',
    #     many=True)
    # tags = serializers.StringRelatedField(many=True, read_only=True)
    ingredients = RecipesIngredientsSerializer(many=True)
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

    # def create(self, validated_data):
    #     print(f'validated_data::: {list(validated_data.values())}')
    #     ingredients_data = validated_data.data.pop('ingredients')
    #     recipe = Recipes.objects.create(**validated_data)
    #     for ingredient_data in ingredients_data:
    #         Ingredient.objects.create(recipe=recipe, **ingredient_data)
    #     return recipe
    # def create(self, validated_data):
    #     print(f'validated_data::::: ')
    #     ingredients_data = validated_data.pop('ingredients')
    #     recipe = Recipes.objects.create(**validated_data)
    #     Ingredient.objects.create(recipe=recipe, **ingredients_data)
    #     return recipe

    # def perform_create(self, serializer):
    #     print(f'serializer::: {serializer}')
    #     # rc2.is_favorited.add(us[3])
    #     """Чтобы передать новое значение для какого-то поля в метод save(),
    #     нужно переопределить метод perform_create().В метод save() в полe
    #     author передадим объект пользователя, отправившего запрос."""
    #     serializer.save(author=self.request.user)

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
