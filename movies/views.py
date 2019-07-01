import secrets

from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import FormView, ListView, DetailView
from rest_framework.generics import get_object_or_404, CreateAPIView, ListAPIView, RetrieveAPIView, \
    RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from movies.forms import UserForm, DownloadForm
from movies.models import Movie, UserUniqueToken, MovieRate
from movies.api.serializer import MovieSerializer
from rest_framework.permissions import IsAuthenticated

from movies.tasks import download_task, send_email


def index(request):
    return render(request, 'index.html')


def single(request):
    return render(request, 'single.html')


def horror(request):
    return render(request, 'horror.html')


def genres(request):
    return render(request, 'genres.html')


def list_view(request):
    return render(request, 'list.html')


def comedy(request):
    return render(request, 'comedy.html')


class DownloadView(FormView):
    template_name = 'download.html'
    form_class = DownloadForm

    def form_valid(self, form):
        option = form.data.get('option')
        movie_name = form.cleaned_data['search']
        download_task.delay(option, movie_name)

        return HttpResponseRedirect(reverse_lazy('movies:index'))


# Despues de login
class BestView(ListView):
    template_name = 'index2.html'
    # extra_context = {'title': 'My Internet movie database'}
    # context_object_name = 'object_list'
    queryset = Movie.objects.all()
    # paginate_by = 6

    def get_queryset(self):
        qs = super(BestView, self).get_queryset()
        return qs.order_by('-id')

    def get_context_data(self, **kwargs):
        data = super(BestView, self).get_context_data(**kwargs)
        best_movie = MovieRate.objects.get_best_rated()
        if best_movie:
            for j in range(len(best_movie)):
                num = str(j)
                movie = Movie.objects.filter(pk=best_movie[j]['movie__id'])
                data.update({
                    'best_rated_movie_' + num: movie,
                    'best_rated_value_' + num: best_movie[j]['rate'],
                })
            return data


# @login_required
class IndexView(ListView):
    template_name = 'principal.html'
    queryset = Movie.objects.all()
    # paginate_by = 6

    def get_queryset(self):
        qs = super(IndexView, self).get_queryset()
        return qs.order_by('-release_date')

    def get_context_data(self, **kwargs):
        data = super(IndexView, self).get_context_data(**kwargs)
        best_movie = MovieRate.objects.get_best_rated()
        if best_movie:
            for j in range(len(best_movie)):
                num = str(j)
                movie = Movie.objects.filter(pk=best_movie[j]['movie__id'])
                data.update({
                    'best_rated_movie_' + num: movie,
                    'best_rated_value_' + num: best_movie[j]['rate'],
                })
            return data


# @login_required
class MovieDetailView(LoginRequiredMixin, DetailView):
    queryset = Movie.objects.all()
    template_name = 'single.html'
    slug_field = 'slug'
    query_pk_and_slug = False

    def get_context_data(self, **kwargs):
        data = super(MovieDetailView, self).get_context_data(**kwargs)
        best_movie = MovieRate.objects.get_best_rated()
        for dic in best_movie:
            # for key, value in dic.items():
            #    print(key, value, dic['rate'])
            if data['movie'].id == dic['movie__id']:
                data.update({
                    'rated_value': dic['rate'],
                })
                return data


class Login(LoginView):
    template_name = 'index.html'

    def form_valid(self, form):
        response = super(Login, self).form_valid(form)
        try:
            UserUniqueToken.objects.get(user_id=self.request.user.pk)
        except UserUniqueToken.DoesNotExist:
            UserUniqueToken.objects.create(token=secrets.token_hex(8), user_id=self.request.user)

        return response


class Logout(LogoutView):
    next_page = '/'
