from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name


class Cookie(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=1)

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

    def __str__(self):
        return self.name


class Nutrition(models.Model):
    cookie = models.OneToOneField(
        Cookie,
        on_delete=models.CASCADE,
        related_name='nutrition'
    )
    calories = models.PositiveIntegerField()
    proteins = models.DecimalField(max_digits=5, decimal_places=2)
    fats = models.DecimalField(max_digits=5, decimal_places=2)
    carbs = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'Пищевая ценность: {self.cookie.name}'
