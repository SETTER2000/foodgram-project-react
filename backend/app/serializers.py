from rest_framework import serializers
from .models import Ingredient, Tag, Recipes
from drf_extra_fields.fields import Base64ImageField


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class RecipesSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        fields = ('id', 'tags', 'ingredients', 'image', 'name', 'text',
                  'cooking_time')
        model = Recipes

    def create(self, validated_data):
        image = validated_data.pop('image')
        data = validated_data.pop('data')
        return Recipes.objects.create(data=data, image=image)
