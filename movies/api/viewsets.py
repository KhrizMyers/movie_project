from rest_framework import viewsets, filters
from movies.models import Movie
from movies.api.serializer import MovieSerializer
from movies.api.pagination import StandardResultsSetPagination


# list GET | retrieve GET | create POST | update PUT | partial_update PATCH | destroy DELETE
class TodoViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'genre', 'release_date', 'country', 'original_language')


"""class MovieView(ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    # def perform_create(self, serializer):
    #    director = get_object_or_404(Movie, id=self.request.data.get('movie_director'))
    #    return serializer.save(director=director)


class MovieDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer"""