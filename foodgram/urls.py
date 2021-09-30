from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from backend.app.views import index

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', index),
    path('api/auth/', include('djoser.urls.authtoken')),
    # если раскомментить будет работать регистрация, НО перестанет работать
    # правильно остальное API.
    path('api/', include('backend.users.urls')),
    path('api/', include('backend.app.urls')),
    path('api/', include('djoser.urls')),

    # path(
    #     'docs/',
    #     TemplateView.as_view(template_name='redoc.html'),
    #     name='redoc',
    # ),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
