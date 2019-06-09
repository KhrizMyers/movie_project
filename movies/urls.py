from django.urls import path
from . import views
from movies.views import index

app_name = 'movies'
urlpatterns = [
    path('',  views.index, name='index'),
    path('single/', views.single, name='single'),
    path('horror/', views.horror, name='horror'),
    path('genres/', views.genres, name='genres'),
    path('comedy/', views.comedy, name='comedy'),
    path('list/', views.list_view, name='list'),
]
