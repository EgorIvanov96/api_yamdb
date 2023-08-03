from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.users import User


class Category(models.Model):
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField('Жанр', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год')
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='categories'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        through='TitleGenre',
        related_name='titles'
    )

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('title', 'genre')


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    titles = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='reviews')


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True)
