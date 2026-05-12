from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator

from .models import Category, Tag, Cookie


class AddCookieForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        min_length=5,
        label='Название печенья',
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        error_messages={
            'min_length': 'Название слишком короткое',
            'required': 'Введите название печенья',
        }
    )

    slug = forms.SlugField(
        max_length=255,
        label='URL',
        validators=[
            MinLengthValidator(5, message='Минимум 5 символов'),
            MaxLengthValidator(100, message='Максимум 100 символов'),
        ]
    )

    description = forms.CharField(
        label='Описание',
        required=False,
        widget=forms.Textarea(attrs={'cols': 50, 'rows': 5})
    )

    price = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        label='Цена'
    )

    status = forms.BooleanField(
        required=False,
        initial=True,
        label='Опубликовано'
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Категория не выбрана'
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        label='Теги'
    )

    def clean_name(self):
        name = self.cleaned_data['name']
        allowed_chars = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
        if not set(name) <= set(allowed_chars):
            raise ValidationError('Название должно содержать только русские буквы, цифры, дефис и пробел.')
        return name

class AddCookieModelForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label='Категория не выбрана',
        label='Категория'
    )

    class Meta:
        model = Cookie

        fields = [
            'name',
            'slug',
            'description',
            'price',
            'category',
            'tags',
            'status',
            'photo',
        ]

        labels = {
            'name': 'Название печенья',
            'slug': 'URL',
            'description': 'Описание',
            'price': 'Цена',
            'category': 'Категория',
            'tags': 'Теги',
            'status': 'Статус',
            'photo': 'Фото',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']

        if len(name) < 3:
            raise ValidationError(
                'Название печенья должно быть не короче 3 символов'
            )

        return name

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Выберите файл')