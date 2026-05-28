from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('about/', views.AboutPage.as_view(), name='about'),

    path('catalog/', views.CookieCatalog.as_view(), name='catalog'),

    path(
        'catalog/category/<int:cat_id>/',
        views.CookieCategory.as_view(),
        name='category'
    ),

    path(
        'tag/<slug:tag_slug>/',
        views.CookieTag.as_view(),
        name='tag'
    ),

    path(
        'catalog/<slug:cookie_slug>/',
        views.CookieDetail.as_view(),
        name='cookie_detail'
    ),

    path('order/', views.CookieCreateView.as_view(), name='order'),

    path(
        'add-cookie/',
        views.AddCookieView.as_view(),
        name='add_cookie'
    ),

    path(
        'upload-file/',
        views.UploadFileView.as_view(),
        name='upload_file'
    ),

    path(
        'cookie/create/',
        views.CookieCreateView.as_view(),
        name='cookie_create'
    ),

    path(
        'cookie/<slug:cookie_slug>/edit/',
        views.CookieUpdateView.as_view(),
        name='cookie_edit'
    ),

    path(
        'cookie/<slug:cookie_slug>/delete/',
        views.CookieDeleteView.as_view(),
        name='cookie_delete'
    ),
]