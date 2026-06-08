from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from .models import Cookie, Category, Tag, Nutrition, Comment, Favorite, CommentReaction


class PriceFilter(admin.SimpleListFilter):
    title = 'Цена товара'
    parameter_name = 'price_group'

    def lookups(self, request, model_admin):
        return [
            ('cheap', 'До 200 руб.'),
            ('expensive', 'От 200 руб.'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'cheap':
            return queryset.filter(price__lt=200)
        if self.value() == 'expensive':
            return queryset.filter(price__gte=200)
        return queryset

  
@admin.register(Cookie)
class CookieAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'category',
        'status',
        'time_create',
        'brief_description',
        'price_with_currency',
        'cookie_photo',
    )
    fields = (
        'name',
        'slug',
        'photo',
        'description',
        'price',
        'category',
        'tags',
        'status',
    )
    list_display_links = ('id', 'name')
    list_editable = ('price', 'status')
    ordering = ('-time_create', 'name')
    list_per_page = 5
    readonly_fields = ('cookie_photo',)
    actions = ('set_published', 'set_draft')
    search_fields = ('name', 'description', 'category__name')
    list_filter = (PriceFilter, 'status', 'category', 'tags')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('tags',)

    @admin.display(description='Краткое описание')
    def brief_description(self, obj):
        return f'{len(obj.description)} символов'

    @admin.display(description='Цена')
    def price_with_currency(self, obj):
        return f'{obj.price} руб.'

    @admin.action(description='Опубликовать выбранные товары')
    def set_published(self, request, queryset):
        count = queryset.update(status=1)
        self.message_user(request, f'Опубликовано товаров: {count}.')

    @admin.action(description='Снять выбранные товары с публикации')
    def set_draft(self, request, queryset):
        count = queryset.update(status=0)
        self.message_user(
            request,
            f'Снято с публикации товаров: {count}.',
            messages.WARNING
        )

    @admin.display(description='Изображение')
    def cookie_photo(self, obj):
        if obj.photo:
            return mark_safe(
                f"<img src='{obj.photo.url}' width='60'>"
            )

        return 'Без фото'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Nutrition)
class NutritionAdmin(admin.ModelAdmin):
    list_display = ('id', 'cookie', 'calories', 'proteins', 'fats', 'carbs')
    list_display_links = ('id', 'cookie')
    search_fields = ('cookie__name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'cookie', 'author', 'time_create')
    list_display_links = ('id', 'cookie')
    search_fields = ('text', 'author__username', 'cookie__name')
    list_filter = ('time_create',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cookie', 'time_create')
    list_display_links = ('id', 'user')
    search_fields = ('user__username', 'cookie__name')
    list_filter = ('time_create',)

@admin.register(CommentReaction)
class CommentReactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'user', 'reaction', 'time_create')
    list_display_links = ('id', 'comment')
    search_fields = ('comment__text', 'user__username')
    list_filter = ('reaction', 'time_create')

