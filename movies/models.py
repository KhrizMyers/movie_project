from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone
from movies.choices import select_genre, ACTION
from movies.queryset import MovieRateQueryset

User = get_user_model()


# Create your models here.
def movie_directory_path(instance, filename):
    return f'movie/{instance.title}/{filename}'


class Movie(models.Model):

    title = models.CharField(max_length=100)
    runtime = models.CharField(max_length=10, null=True)
    poster = models.ImageField(upload_to=movie_directory_path)
    img = models.ImageField(upload_to=movie_directory_path, null=True, blank=True)
    detail = models.TextField(max_length=250)
    trailer = models.URLField(null=True, blank=True)
    genre = models.CharField(max_length=40, choices=select_genre, default=ACTION)
    original_language = models.CharField(max_length=20)
    release_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=15)  # libreria django-cities
    movie_director = models.ManyToManyField('MovieDirector')
    movie_actor = models.ManyToManyField('MovieActor')
    slug = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return '{0}, {1}, {2}, {3}, {4}, {5}, {6}'.format(self.title, self.detail, self.trailer, self.genre, self.original_language, self.movie_director, self.movie_actor)

    def get_absolute_url(self):
        return reverse_lazy('movies:movie-detail', args=(self.title, ))


class MovieRate(models.Model):
    rate = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=5)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)  # settings.AUTH_USER_MODEL
    comment = models.TextField(max_length=150)

    objects = MovieRateQueryset.as_manager()

    class Meta:
        unique_together = ('user', 'movie')
        permissions = (
            ('can_vote_two_times', 'Can vote two times'),
        )

    def __str__(self):
        return f'{self.user} : {self.rate}'


class MovieDirector(models.Model):
    name = models.CharField(max_length=30)
    age = models.SmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['name', 'age']

    def __str__(self):
        return '{0}, {1}'.format(self.name, self.age)


class MovieActor(models.Model):
    name = models.CharField(max_length=150)
    age = models.SmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['name', 'age']

    def __str__(self):
        return '{0}, {1}'.format(self.name, self.age)


class UserUniqueToken(models.Model):
    user_id = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    datetime = models.DateTimeField(auto_now_add=timezone.now)
