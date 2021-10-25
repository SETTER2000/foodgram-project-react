from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

DEBUG = settings.DEBUG

extra_patterns = [
    path("", include("users.urls")),
    path("", include("app.urls")),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(extra_patterns)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
