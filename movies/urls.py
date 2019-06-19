from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from movies.api.viewsets import TodoViewSet
from . import views
from movies.views import index, IndexView, Login, Logout

app_name = 'movies'
urlpatterns = [
    path('', Login.as_view(), name="login"),
    path('', Logout.as_view(), name="logout"),
    path('principal/',  IndexView.as_view(), name='index'),
    path('single/', views.single, name='single'),
    path('horror/', views.horror, name='horror'),
    path('genres/', views.genres, name='genres'),
    path('comedy/', views.comedy, name='comedy'),
    path('list/', views.list_view, name='list'),
    path('poster/', views.movie_list, name='list_poster'),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth')
]
