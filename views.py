import os
import uuid

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import (
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import AddCookieForm, AddCookieModelForm, UploadFileForm
from .models import Cookie, Category, Tag
from .utils import DataMixin


class HomePage(DataMixin, TemplateView):
    template_name = 'shop/home.html'
    title_page = 'Главная страница'


class AboutPage(DataMixin, TemplateView):
    template_name = 'shop/about.html'
    title_page = 'О сайте'


class CookieCatalog(DataMixin, ListView):
    model = Cookie
    template_name = 'shop/catalog.html'
    context_object_name = 'cookies'
    title_page = 'Каталог печенья'

    def get_queryset(self):
        sort = self.request.GET.get('sort')

        cookies = Cookie.objects.filter(status=1).select_related(
            'category'
        ).prefetch_related('tags')

        if sort == 'name':
            return cookies.order_by('name')

        if sort == 'price':
            return cookies.order_by('price')

        return cookies.order_by('-time_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = Category.objects.all()

        return self.get_mixin_context(context)


class CookieCategory(DataMixin, ListView):
    template_name = 'shop/catalog.html'
    context_object_name = 'cookies'
    allow_empty = False

    def get_queryset(self):
        return Cookie.objects.filter(
            category_id=self.kwargs['cat_id'],
            status=1
        ).select_related('category').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs['cat_id'])

        return self.get_mixin_context(
            context,
            title=f'Категория: {category.name}'
        )


class CookieTag(DataMixin, ListView):
    template_name = 'shop/catalog.html'
    context_object_name = 'cookies'
    allow_empty = False

    def get_queryset(self):
        return Cookie.objects.filter(
            tags__slug=self.kwargs['tag_slug'],
            status=1
        ).select_related('category').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])

        return self.get_mixin_context(
            context,
            title=f'Тег: {tag.name}'
        )


class CookieDetail(DataMixin, DetailView):
    model = Cookie
    template_name = 'shop/cookie_detail.html'
    context_object_name = 'cookie'
    slug_url_kwarg = 'cookie_slug'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Cookie.objects.select_related('category').prefetch_related('tags'),
            slug=self.kwargs[self.slug_url_kwarg],
            status=1
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return self.get_mixin_context(
            context,
            title=context['cookie'].name
        )


class AddCookieView(
    PermissionRequiredMixin,
    LoginRequiredMixin,
    DataMixin,
    View
):
    permission_required = 'shop.add_cookie'
    raise_exception = True
    title_page = 'Добавление печенья через View'

    def get(self, request):
        form = AddCookieForm()

        return render(request, 'shop/add_cookie.html', {
            'form': form,
            'title': self.title_page
        })

    def post(self, request):
        form = AddCookieForm(request.POST)

        if form.is_valid():
            cookie = Cookie.objects.create(
                name=form.cleaned_data['name'],
                slug=form.cleaned_data['slug'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price'],
                status=1 if form.cleaned_data['status'] else 0,
                category=form.cleaned_data['category']
            )

            cookie.tags.set(form.cleaned_data['tags'])

            return redirect('catalog')

        return render(request, 'shop/add_cookie.html', {
            'form': form,
            'title': self.title_page
        })


def handle_uploaded_file(file):
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

    name, ext = os.path.splitext(file.name)
    unique_name = f'{name}_{uuid.uuid4().hex}{ext}'

    with open(f'uploads/{unique_name}', 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return unique_name


class UploadFileView(LoginRequiredMixin, DataMixin, FormView):
    form_class = UploadFileForm
    template_name = 'shop/upload_file.html'
    success_url = reverse_lazy('upload_file')
    title_page = 'Загрузка файла'

    def form_valid(self, form):
        handle_uploaded_file(form.cleaned_data['file'])
        return super().form_valid(form)


class CookieCreateView(
    PermissionRequiredMixin,
    LoginRequiredMixin,
    DataMixin,
    CreateView
):
    permission_required = 'shop.add_cookie'
    raise_exception = True

    form_class = AddCookieModelForm
    template_name = 'shop/add_cookie.html'
    success_url = reverse_lazy('catalog')
    title_page = 'Добавление печенья через CreateView'


class CookieUpdateView(
    PermissionRequiredMixin,
    LoginRequiredMixin,
    DataMixin,
    UpdateView
):
    permission_required = 'shop.change_cookie'
    raise_exception = True

    model = Cookie
    form_class = AddCookieModelForm
    template_name = 'shop/add_cookie.html'
    success_url = reverse_lazy('catalog')
    slug_url_kwarg = 'cookie_slug'
    title_page = 'Редактирование печенья'


class CookieDeleteView(
    PermissionRequiredMixin,
    LoginRequiredMixin,
    DataMixin,
    DeleteView
):
    permission_required = 'shop.delete_cookie'
    raise_exception = True

    model = Cookie
    template_name = 'shop/cookie_confirm_delete.html'
    success_url = reverse_lazy('catalog')
    slug_url_kwarg = 'cookie_slug'
    context_object_name = 'cookie'
    title_page = 'Удаление печенья'


def page_not_found(request, exception):
    return render(request, 'shop/404.html', status=404)