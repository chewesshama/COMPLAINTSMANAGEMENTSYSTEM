from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from complaints.views import custom_404_view, custom_403_view, custom_500_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('complaints.urls'), name="complaints"),
    
]

handler403 = custom_403_view
handler404 = custom_404_view
handler500 = custom_500_view

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
     
     
     