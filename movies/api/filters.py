import django_filters
from movies.models import Movie


class ManagerFilter(django_filters.FilterSet):
    class Meta:
        model = Movie
        fields = {'title': ['exact', 'in', 'startswith']}

