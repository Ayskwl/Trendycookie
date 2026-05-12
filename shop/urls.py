from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('about/', views.about, name='about'),
    path('order/', views.order, name='order'),
    path('order/success/', views.order_success, name='order_success'),
    path('tag/<slug:tag_slug>/', views.show_tag, name='tag'),
    path('catalog/<slug:cookie_slug>/', views.cookie_detail, name='cookie_detail'),
    path('catalog/category/<int:cat_id>/', views.category, name='category'),
    path('add-cookie/', views.add_cookie, name='add_cookie'),
    path('add-cookie-model/', views.add_cookie_model, name='add_cookie_model'),
    path('upload-file/', views.upload_file, name='upload_file'),
]
