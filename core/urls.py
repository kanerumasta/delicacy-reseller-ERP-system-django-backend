
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('auth/', include('authentication.urls')),

    path('inventory/', include('inventory.urls')),

    path('requisition/', include('requisition.urls')),

    path('purchasing/', include('purchasing.urls')),
    path('logs/', include('logs.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)