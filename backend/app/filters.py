import django_filters
from django_filters.rest_framework import filters

from .models import Recipes


class RecipesFilter(django_filters.FilterSet):
    # year = filters.NumberFilter(field_name='year', lookup_expr='exact')
    # name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    tags = django_filters.CharFilter(
        field_name='tags__slug',
        lookup_expr='iexact'
    )

    # class Meta:
    #     model = Recipes
    #     fields = '__all__'

    # genre = django_filters.CharFilter(
    #     field_name='genre__slug',
    #     lookup_expr='iexact'
    # )
    #
    # class Meta:
    #     model = Title
    #     fields = '__all__'
    # pass
