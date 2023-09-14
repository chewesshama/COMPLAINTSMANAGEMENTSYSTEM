from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("complaints.urls"), name="complaints"),
    #    re_path(r'^.*$', custom_404_view)
]

handler404 = "complaints.views.custom_404_view"
handler403 = "complaints.views.custom_403_view"
handler500 = "complaints.views.custom_500_view"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
