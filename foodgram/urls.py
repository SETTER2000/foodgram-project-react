from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include('backend.users.urls')),
    # path('api/', include('backend.app.urls')),
    # path('api/', include('backend.users.urls', namespace='backend.users')),
    path('api/', include('backend.app.urls', namespace='backend.app')),
    path('api/', include('djoser.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
