from app.views import (FavoriteModelViewSet, IngredientModelViewSet,
                       RecipesModelViewSet, ShoppingCardModelViewSet,
                       TagModelViewSet, download_pdf)
from django.urls import path
from rest_framework import routers

app_name = 'backend.app'
router_v1 = routers.DefaultRouter()

router_v1.register(r'ingredients', IngredientModelViewSet,
                   basename='ingredients')
router_v1.register(r'tags', TagModelViewSet, basename='tags')
router_v1.register(r'recipes', RecipesModelViewSet, basename='recipes')
router_v1.register(r'recipes/(?P<id>[0-9]+)/favorite',
                   FavoriteModelViewSet, basename='favorite')
router_v1.register(r'recipes/(?P<id>[0-9]+)/shopping_cart',
                   ShoppingCardModelViewSet, basename='shopping_cart')

urlpatterns = [
    path('recipes/download_shopping_cart/', download_pdf,
         name='download_pdf')]

urlpatterns += router_v1.urls
