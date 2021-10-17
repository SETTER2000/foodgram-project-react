from django.urls import include, re_path
from rest_framework import routers

from . import views as vs

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', vs.UserModelViewSet, basename='users')
router_v1.register(r'users/subscriptions', vs.SubscriptionsModelViewSet,
                   basename='users')
router_v1.register(r'users/(?P<id>[0-9]+)/subscribe',
                   vs.SubscriptionsModelViewSet,
                   basename='users')

urlpatterns = [re_path(r'^', include(router_v1.urls)), ]
