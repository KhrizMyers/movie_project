from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from movies.api.viewsets import TodoViewSet
from . import views
from movies.views import Login, Logout, BestView, IndexView, MovieDetailView, DownloadView

app_name = 'movies'
urlpatterns = [
    path('', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('principal/',  IndexView.as_view(), name='index'),
    path('best/',  BestView.as_view(), name='index2'),
    # path('single/', views.single, name='single'),
    path('movie/<slug>/', MovieDetailView.as_view(), name='single'),
    # path('movie/<slug>/', MovieDetailView.as_view(), name='movie-detail'),
    path('horror/', views.horror, name='horror'),
    path('genres/', views.genres, name='genres'),
    path('comedy/', views.comedy, name='comedy'),
    path('list/', views.list_view, name='list'),
    path('download/', DownloadView.as_view(), name='download'),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth')
]
