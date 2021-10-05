from django.urls import include, path, re_path
from rest_framework import routers
from . import views as vs

app_name = 'backend.users'

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', vs.UserModelViewSet, basename='users')
router_v1.register(r'users/subscriptions', vs.SubscriptionsModelViewSet,
                   basename='users')


urlpatterns = [
    re_path(r'^', include(router_v1.urls)),
    # path('auth/email/', email_auth, name='email_auth'),

]
