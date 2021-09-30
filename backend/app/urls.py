from django.urls import include, path, re_path
from rest_framework import routers
from . import views as vs

router_v1 = routers.DefaultRouter()

router_v1.register(r'ingredients', vs.IngredientModelViewSet,
                   basename='ingredients')
router_v1.register(r'tags', vs.TagModelViewSet, basename='tags')
router_v1.register(r'recipes', vs.RecipesModelViewSet, basename='recipes')
router_v1.register(r'recipes/(?P<id>[0-9]+)/favorite',
                   vs.FavoriteModelViewSet, basename='favorite')

urlpatterns = [
    # re_path(r'^', include(router_v1.urls)),
]

urlpatterns += router_v1.urls
