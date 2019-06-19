import secrets

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import FormView
from rest_framework.generics import get_object_or_404, CreateAPIView, ListAPIView, RetrieveAPIView, \
    RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from movies.forms import UserForm
from movies.models import Movie, UserUniqueToken
from movies.api.serializer import MovieSerializer
from rest_framework.permissions import IsAuthenticated


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


def movie_list(request):
    movie = Movie.objects.all()
    context = {'movie_list': movie}
    return render(request, 'base.html', context)


# Despues de login
class IndexView(generic.ListView):
    template_name = 'principal.html'
    context_object_name = 'movie_list'

    def get_queryset(self):
        # return Item.objects.order_by('-rating')[:5]
        return Movie.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context['slider'] = Movie.objects.all()
        return context


class Login(LoginView):
    template_name = 'index.html'

    def form_valid(self, form):
        print(self.request.user)
        try:
            UserUniqueToken.objects.get(user_id=self.request.user.pk)
        except UserUniqueToken.DoesNotExist:
            UserUniqueToken.objects.create(token=secrets.token_hex(8), user_id=self.request.user)

        return super(Login, self).form_valid(form)


class Logout(LogoutView):
    pass
# @login_required
# def user_form(request, token):
#     user_token = get_object_or_404(UserUniqueToken, token=token)
#     if not user_token.user_id == request.user.id:
#         print("Error: tokens not match")
#
#     time_now = timezone.now()
#     if user_token.datetime > (time_now - timedelta(hours=2)):
#         print("Preparing for logout")
#
#     return render(request, 'index.html')
