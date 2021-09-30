import os, base64, time
from foodgram.settings import MEDIA_ROOT, SUB_DIR_RECIPES,MEDIA_URL
from coreapi.exceptions import ParseError
from .models import Ingredient, Tag, Recipes, User
from rest_framework import serializers
from django.contrib.auth import get_user_model


class Base64ImageFieldToFile(serializers.Field):
    """ Новый тип поля в serializers.py. для преобразования base64 в файл."""

    def to_representation(self, value):
        """Для чтения."""
        print(f'KKKKKKKKKK8:::{value}')
        filename = value
        value = f'{MEDIA_ROOT}/{value}'
        # f = open(value, "rb")
        with open(value, 'rb') as f:
            str_64 = base64.standard_b64encode(f.read())
        value = (('%s' % str_64.decode().strip()))

        # print(f'RESPOSE IMG::: data:image/jpeg;base64,{value}')
        b64 = f'data:image/jpeg;base64,{value}'
        # url = f'media/{value}'
        # print(f'MEDIA_URL IMG:::{url}')
        print(f'RESPOSE IMG:::{filename}')
        return f'/media/{filename}'

    # base64_str = base64.encodestring(('%s:%s' % (username,password)).encode()).decode().strip()
    def to_internal_value(self, data):
        """Для записи."""
        print(f'SSSSS::: {data}')
        dir = f'{MEDIA_ROOT}/{SUB_DIR_RECIPES}'
        os.makedirs(dir, exist_ok=True)
        try:
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            img_data = base64.b64decode(imgstr)
            filename = f'{SUB_DIR_RECIPES}/{int(time.time())}.{ext}'
            full_file_path = f'{MEDIA_ROOT}/{filename}'
            print(f'full_file_path:: {full_file_path}')
            # with open(full_file_path, 'wb') as f:
            #     f.write(img_data)
            f = open(full_file_path, 'wb')
            f.write(img_data)
            f.close()
        except ValueError:
            raise serializers.ValidationError('С картинкой проблемы.')
        # Возвращаем данные в новом формате
        print(f'QQQQQQQQQ:: {filename}')
        return filename


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField()
    # author = serializers.SerializerMethodField()
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
            'cooking_time')

        model = Recipes

    def get_author(self, obj):
        #
        print(f'GGGGGGGG::: {obj}')
        user = User.objects.filter(pk=obj.author_id)
        if user is None:
            raise ParseError("Неверный запрос!")
        print(f'ASSSSSQQQQQQQQQQ::: {user}')
        return user

    def get_ingredients(self, obj):
        response = []
        for _ingredient in obj.ingredients.all():
            print(f'RRRRROO::: {_ingredient}')
            ingredients_profile = IngredientSerializer(_ingredient, context={
                'request': self.context['request']})
            response.append(ingredients_profile.data)
        return response

    # def to_internal_value(self, data):
    #     """Для записи."""
    #     print(f'SSSSS::: {data}')
    #     dir = f'{MEDIA_ROOT}/recipes'
    #     os.makedirs(dir, exist_ok=True)
    #     try:
    #         format, imgstr = data['image'].split(';base64,')
    #         ext = format.split('/')[-1]
    #         img_data = base64.b64decode(imgstr)
    #         data = f'{dir}/{int(time.time())}.{ext}'
    #         with open(data, 'wb') as f:
    #             f.write(img_data)
    #     except ValueError:
    #         raise serializers.ValidationError('С картинкой проблемы.')
    #     # Возвращаем данные в новом формате
    #     print(f'QQQQQQQQQ:: {data}')
    #     return data

    def create(self, validated_data):
        return Recipes.objects.create(**validated_data)
    # def create(self, validated_data):
    #     print(f'DDDDDDDDDDDDDD::; {validated_data}')
    #     image = validated_data.pop('image')
    #     data = validated_data.pop('data')
    #     return Recipes.objects.create(data=data, image=image)

    # def to_internal_value(self, data):
    #     image = data['image']
    #
    #     # format, imgstr = image.split(';base64,')
    #     # ext = format.split('/')[-1]
    #     print(f'AAAAAAAAAAAAAAAAAA::: {data}')
    #     # serializer = UploadedBase64ImageSerializer(data={'file': image})
    #     # dt = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
    #     # data['image'] = dt
    #     # print(f'FFFFF::: {serializer}')
    #     return super(RecipesSerializer, self).to_internal_value(data)

    # def create(self, validated_data):
    #     image = validated_data.pop('image')
    #     # print(f'DDDDDDDD::{validated_data}')
    #     # print(f'DDDaaaaaasss::{self}')
    #     data = validated_data.pop('data')
    #     # return Recipes.objects.create(image=image)
    #     return Recipes.objects.create(validated_data, image=image)
