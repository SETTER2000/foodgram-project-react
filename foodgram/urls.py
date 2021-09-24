from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/', include('djoser.urls.authtoken')),
    # если раскомментить будет работать регистрация, НО перестанет работать
    # правильно остальное API.
    # path('api/', include('backend.users.urls')),
    path('api/', include('djoser.urls')),

    # path(
    #     'docs/',
    #     TemplateView.as_view(template_name='redoc.html'),
    #     name='redoc',
    # ),
]
