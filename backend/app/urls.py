from django.urls import path
from rest_framework import routers
from . import views as vs

app_name = 'backend.app'

# recipes_list = vs.RecipesModelViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# recipes_detail = vs.RecipesModelViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
# recipes_highlight = vs.RecipesModelViewSet.as_view({
#     'get': 'highlight'
# }, renderer_classes=[renderers.StaticHTMLRenderer])
# recipes_highlight = vs.RecipesModelViewSet.as_view({
#     'get': 'highlight'
# }, renderer_classes=[renderers.StaticHTMLRenderer])
# user_list = UserViewSet.as_view({
#     'get': 'list'
# })
# user_detail = UserViewSet.as_view({
#     'get': 'retrieve'
# })

router_v1 = routers.DefaultRouter()

router_v1.register(r'ingredients', vs.IngredientModelViewSet,
                   basename='ingredients')
router_v1.register(r'tags', vs.TagModelViewSet, basename='tags')
router_v1.register(r'recipes', vs.RecipesModelViewSet, basename='recipes')
router_v1.register(r'recipes/(?P<id>[0-9]+)/favorite',
                   vs.FavoriteModelViewSet, basename='favorite')
router_v1.register(r'recipes/(?P<id>[0-9]+)/shopping_cart',
                   vs.ShoppingCardModelViewSet, basename='shopping_cart')

# router_v1.register(r'recipes/download_shopping_cart',
#                    vs.download_pdf.as_view(), basename='download_pdf')

urlpatterns = [
    # re_path(r'^', include(router_v1.urls)),
    path('recipes/download_shopping_cart/',  vs.download_pdf,
         name='download_pdf')

]

urlpatterns += router_v1.urls
