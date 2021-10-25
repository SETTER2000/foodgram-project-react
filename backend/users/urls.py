from django.urls import include, path
from rest_framework import routers

from users.views import UserModelViewSet

router = routers.DefaultRouter()
router.register('users', UserModelViewSet, basename='users')
# router.register(r'users/subscriptions', vs.SubscriptionsModelViewSet,
#                    basename='users')
# router.register(r'users/(?P<id>[0-9]+)/subscribe',
#                    vs.SubscriptionsModelViewSet,
#                    basename='users')

# urlpatterns = [re_path(r'^', include(router.urls)), ]

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]