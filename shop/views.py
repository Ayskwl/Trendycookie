from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Cookie


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