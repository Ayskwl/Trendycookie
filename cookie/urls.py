from django.contrib import admin
from django.urls import path, include
from shop.views import page_not_found
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
]

handler404 = page_not_found

admin.site.site_header = 'Панель администрирования Trendy cookies'
admin.site.index_title = 'Управление каталогом печенья'
admin.site.site_title = 'Trendy cookies'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)