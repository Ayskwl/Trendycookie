from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('about/', views.about, name='about'),
    path('order/', views.order, name='order'),
    path('order/success/', views.order_success, name='order_success'),

    path('catalog/<slug:cookie_slug>/', views.cookie_detail, name='cookie_detail'),
    path('catalog/category/<int:cat_id>/', views.category, name='category'),
    path('old-catalog/', views.old_catalog_redirect, name='old_catalog'),
]