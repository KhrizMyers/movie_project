from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.db import models
from movies.choices import select_genre, ACTION

User = get_user_model()


# Create your models here.
def movie_directory_path(instance, filename):
    return f'movie/{instance.title}/{filename}'


class Movie(models.Model):

    title = models.CharField(max_length=50)
    runtime = models.SmallIntegerField(null=True, blank=False)
    poster = models.ImageField(upload_to=movie_directory_path)
    detail = models.TextField(max_length=150)
    trailer = models.URLField()
    genre = models.CharField(max_length=40, choices=select_genre, default=ACTION)
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    original_language = models.CharField(max_length=20)
    release_date = models.DateField()
    country = models.CharField(max_length=15)  # libreria django-cities
    movie_director = models.ManyToManyField('MovieDirector')
    movie_actor = models.ManyToManyField('MovieActor')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return '{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}'.format(self.title, self.detail, self.trailer, self.genre, self.rating, self.original_language, self.movie_director, self.movie_actor)


class MovieRate(models.Model):
    rate = models.PositiveSmallIntegerField(null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  # settings.AUTH_USER_MODEL
    comment = models.TextField(max_length=150)

    def __str__(self):
        return '{0}'.format(self.comment)


class MovieDirector(models.Model):
    name = models.CharField(max_length=30)
    age = models.SmallIntegerField()

    class Meta:
        ordering = ['name', 'age']

    def __str__(self):
        return '{0}, {1}'.format(self.name, self.age)


class MovieActor(models.Model):
    name = models.CharField(max_length=30)
    age = models.SmallIntegerField()

    class Meta:
        ordering = ['name', 'age']

    def __str__(self):
        return '{0}, {1}'.format(self.name, self.age)
