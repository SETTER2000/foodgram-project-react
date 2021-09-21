from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),

    # path(
    #     'docs/',
    #     TemplateView.as_view(template_name='redoc.html'),
    #     name='redoc',
    # ),
]
