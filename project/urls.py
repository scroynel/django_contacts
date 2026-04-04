from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', include('contacts.urls'))
] 

urlpatterns += static(settings.STATIC_URL, documents_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, documents_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
#     try:
#         import debug_toolbar

#         urlpatterns += [
#             path("__debug__/", include("debug_toolbar.urls")),
#         ]
#     except ImportError:
#         pass