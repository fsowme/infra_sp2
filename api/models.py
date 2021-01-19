import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

ADMIN = "admin"
USER = "user"
MODERATOR = "moderator"

role_choices = [
    (USER, "User"),
    (MODERATOR, "Moderator"),
    (ADMIN, "Administrator"),
]


def today_year():
    return int(datetime.date.today().year)


class User(AbstractUser):
    role = models.CharField(
        max_length=10,
        choices=role_choices,
        default=USER,
        verbose_name="Права пользователя",
    )
    email = models.EmailField(
        max_length=50, unique=True, blank=False, verbose_name="Email адресс"
    )
    first_name = models.CharField(
        max_length=30, blank=True, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=30, blank=True, verbose_name="Фамилия"
    )
    bio = models.TextField(max_length=200, blank=True, verbose_name="О себе")
    confirmation_code = models.CharField(
        max_length=70, unique=True, blank=True, null=True
    )

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField(max_length=255, verbose_name="Жанр")
    slug = models.SlugField(
        blank=True, unique=True, verbose_name="Адрес жанра"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Категория")
    slug = models.SlugField(
        blank=True, unique=True, verbose_name="Адрес категории"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        unique=True, max_length=255, verbose_name="Произведение"
    )
    year = models.IntegerField(
        blank=True,
        null=True,
        db_index=True,
        validators=[MaxValueValidator(today_year())],
        verbose_name="Год выпуска",
    )
    description = models.TextField(verbose_name="Описание")
    genre = models.ManyToManyField(
        Genre, blank=True, related_name="titles", verbose_name="Жанр"
    )
    category = models.ForeignKey(
        Category,
        models.SET_NULL,
        blank=True,
        null=True,
        related_name="titles",
        verbose_name="Категория",
    )

    class Meta:
        ordering = ["-year"]

    def genre_for_admin(self):
        result = "(None)"
        if self.genre.exists():
            result = [genre.name for genre in self.genre.all()]
        return result

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
    )
    text = models.TextField(null=False, verbose_name="Отзыв")
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации", auto_now_add=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Оценка",
    )

    class Meta:
        unique_together = ["author", "title"]
        ordering = ["-pub_date"]

    def __str__(self):
        return f"{self.id}"


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )
    text = models.TextField(verbose_name="Комментарий")
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации", auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
    )

    class Meta:
        ordering = ["-pub_date"]
