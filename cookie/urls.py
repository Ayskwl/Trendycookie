from django.contrib import admin
from django.urls import path, include
from shop.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
]

handler404 = page_not_found