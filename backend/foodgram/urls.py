from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from backend.app.views import index

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', index),
    path('api/auth/', include('djoser.urls.authtoken')),
<<<<<<< HEAD:backend/foodgram/urls.py
    path('api/', include('backend.users.urls')),
    # path('api/', include('backend.app.urls')),
    # path('api/', include('backend.users.urls', namespace='backend.users')),
    path('api/', include('backend.app.urls', namespace='backend.app')),

=======
    path('api/', include('users.urls')),
    # path('api/', include('api.urls')),
    # path('api/', include('users.urls', namespace='users')),
    path('api/', include('api.urls', namespace='api')),
>>>>>>> olga:foodgram/urls.py
    path('api/', include('djoser.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
