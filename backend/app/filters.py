# import django_filters
from django_filters import rest_framework as filters

from .models import Recipes, Tag


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class RecipesFilter(filters.FilterSet):
    # year = filters.NumberFilter(field_name='year', lookup_expr='exact')
    # name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    tags = CharFilterInFilter(field_name='tags__slug')

    class Meta:
        model = Recipes
        fields = ('tags',)

    # genre = django_filters.CharFilter(
    #     field_name='genre__slug',
    #     lookup_expr='iexact'
    # )
    #
    # class Meta:
    #     model = Title
    #     fields = '__all__'
    # pass
