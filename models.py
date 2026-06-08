from django.db import models
from django.urls import reverse
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Cookie(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=1)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cookies',
        verbose_name='Автор',
        null=True,
        blank=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='cookies',
        null=True,
        blank=True
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='cookies'
    )

    photo = models.ImageField(
        upload_to='photos/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name='Фото'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Печенье'
        verbose_name_plural = 'Печенье'
        permissions = [
            ('can_publish_cookie', 'Может публиковать печенье'),
        ]

    class Meta:
        verbose_name = 'Пищевая ценность'
        verbose_name_plural = 'Пищевая ценность'


class Nutrition(models.Model):
    cookie = models.OneToOneField(
        Cookie,
        on_delete=models.CASCADE,
        related_name='nutrition',
        verbose_name='Печенье'
    )

    calories = models.PositiveIntegerField(
        verbose_name='Калории'
    )

    proteins = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Белки'
    )

    fats = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Жиры'
    )

    carbs = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='Углеводы'
    )

    def __str__(self):
        return f'Пищевая ценность: {self.cookie.name}'

    class Meta:
        verbose_name = 'Пищевая ценность'
        verbose_name_plural = 'Пищевая ценность'


class Comment(models.Model):
    cookie = models.ForeignKey(
        Cookie,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Печенье'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )

    text = models.TextField(verbose_name='Текст комментария')
    time_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-time_create']

    def __str__(self):
        return f'Комментарий от {self.author}'


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )

    cookie = models.ForeignKey(
        Cookie,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Печенье'
    )

    time_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ('user', 'cookie')

    def __str__(self):
        return f'{self.user} — {self.cookie}'

   
class CommentReaction(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'

    REACTION_CHOICES = [
        (LIKE, 'Лайк'),
        (DISLIKE, 'Дизлайк'),
    ]

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='reactions',
        verbose_name='Комментарий'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comment_reactions',
        verbose_name='Пользователь'
    )

    reaction = models.CharField(
        max_length=10,
        choices=REACTION_CHOICES,
        verbose_name='Реакция'
    )

    time_create = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата реакции'
    )

    class Meta:
        verbose_name = 'Реакция на комментарий'
        verbose_name_plural = 'Реакции на комментарии'
        unique_together = ('comment', 'user')

    def __str__(self):
        return f'{self.user} — {self.comment} — {self.reaction}'
