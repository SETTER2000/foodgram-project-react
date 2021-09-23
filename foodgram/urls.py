from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include('backend.users.urls')),
    # path('api/auth/token/login/', include('djoser.urls.jwt')),
    # path(
    #     'docs/',
    #     TemplateView.as_view(template_name='redoc.html'),
    #     name='redoc',
    # ),
]
