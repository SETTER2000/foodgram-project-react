from django.urls import include, path, re_path
from rest_framework import routers
from . import views as vs

router_v1 = routers.DefaultRouter()

router_v1.register(r'ingredients', vs.IngredientModelViewSet,
                   basename='ingredients')
router_v1.register(r'tags', vs.TagModelViewSet,basename='tags')
router_v1.register(r'recipes', vs.RecipesModelViewSet,basename='recipes')


urlpatterns = [
    re_path(r'^', include(router_v1.urls)),
]
