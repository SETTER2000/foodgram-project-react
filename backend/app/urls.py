from django.urls import path
from rest_framework import routers

from . import views as vs

app_name = 'backend.app'
router_v1 = routers.DefaultRouter()

router_v1.register(r'ingredients', vs.IngredientModelViewSet,
                   basename='ingredients')
router_v1.register(r'tags', vs.TagModelViewSet, basename='tags')
router_v1.register(r'recipes', vs.RecipesModelViewSet, basename='recipes')
router_v1.register(r'recipes/(?P<id>[0-9]+)/favorite',
                   vs.FavoriteModelViewSet, basename='favorite')
router_v1.register(r'recipes/(?P<id>[0-9]+)/shopping_cart',
                   vs.ShoppingCardModelViewSet, basename='shopping_cart')

urlpatterns = [
    path('recipes/download_shopping_cart/', vs.download_pdf,
         name='download_pdf')]

urlpatterns += router_v1.urls
