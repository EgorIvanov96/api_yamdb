from django.db import models

from users.users import User


class Category(models.Model):
<<<<<<< HEAD
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50, unique=True)
=======
    name = models.TextField('Категория', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50)
>>>>>>> feature/genres

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField('Жанр', max_length=256)
    slug = models.SlugField('Идентификатор', max_length=50)

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField('Оценка')

    def __str__(self):
        return self.text


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
        null=True,
        related_name='genres'
    )
    reviews = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        null=True,
        related_name='reviews'
    )

    def __str__(self):
        return self.text


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
