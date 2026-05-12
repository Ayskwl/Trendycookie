from django import forms
from .forms import AddCookieForm, AddCookieModelForm, UploadFileForm
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Cookie, Tag
import uuid
import os


class OrderForm(forms.Form):
    name = forms.CharField(
        label='Имя',
        max_length=100
    )
    phone = forms.CharField(
        label='Телефон',
        max_length=20
    )
    address = forms.CharField(
        label='Адрес',
        widget=forms.Textarea
    )
    cookie_type = forms.CharField(
        label='Вид печенья',
        max_length=100
    )
    quantity = forms.IntegerField(
        label='Количество',
        min_value=1
    )


cookies_data = [
    {
        "id": 1,
        "name": "Шоколадное печенье",
        "slug": "chocolate-cookie",
        "price": 120
    },
    {
        "id": 2,
        "name": "Овсяное печенье",
        "slug": "oatmeal-cookie",
        "price": 90
    },
    {
        "id": 3,
        "name": "Имбирное печенье",
        "slug": "ginger-cookie",
        "price": 150
    },
]


def home(request):
    return render(request, 'shop/home.html')


def catalog(request):
    sort = request.GET.get('sort')
    cookies = Cookie.objects.all()

    if sort == 'name':
        cookies = cookies.order_by('name')
    elif sort == 'price':
        cookies = cookies.order_by('price')

    return render(request, 'shop/catalog.html', {'cookies': cookies})


def about(request):
    return render(request, 'shop/about.html')


def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            return redirect('order_success')
    else:
        form = OrderForm()

    context = {
        'form': form,
    }
    return render(request, 'shop/order.html', context)


def order_success(request):
    return render(request, 'shop/order_success.html')


def cookie_detail(request, cookie_slug):
    cookie = get_object_or_404(Cookie, slug=cookie_slug)
    return render(request, 'shop/cookie_detail.html', {'cookie': cookie})


def category(request, cat_id):
    return HttpResponse(
        f'<h1>Категория печенья</h1><p>ID категории: {cat_id}</p>'
    )


def old_catalog_redirect(request):
    return redirect('catalog')


def confirm_order(request, code):
    return HttpResponse(
        f'<h1>Подтверждение заказа</h1><p>Код заказа: {code}</p>'
    )


def page_not_found(request, exception):
    return render(request, 'shop/404.html', status=404)


def show_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    cookies = tag.cookies.filter(status=1)

    return render(request, 'shop/catalog.html', {
        'cookies': cookies,
        'page_title': f'Тег: {tag.name}'
    })


def add_cookie(request):
    if request.method == 'POST':
        form = AddCookieForm(request.POST)

        if form.is_valid():
            try:
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
            except:
                form.add_error(None, 'Ошибка добавления товара')
    else:
        form = AddCookieForm()

    return render(request, 'shop/add_cookie.html', {
        'form': form,
        'title': 'Добавление печенья'
    })

def add_cookie_model(request):
    if request.method == 'POST':
        form = AddCookieModelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('catalog')
    else:
        form = AddCookieModelForm()

    return render(request, 'shop/add_cookie.html', {
        'form': form,
        'title': 'Добавление печенья через ModelForm'
    })


def handle_uploaded_file(f):
    name, ext = os.path.splitext(f.name)
    unique_name = f'{name}_{uuid.uuid4().hex}{ext}'

    with open(f'uploads/{unique_name}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return unique_name

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            handle_uploaded_file(form.cleaned_data['file'])
            return redirect('upload_file')
    else:
        form = UploadFileForm()

    return render(request, 'shop/upload_file.html', {
        'form': form,
        'title': 'Загрузка файла'
    })
