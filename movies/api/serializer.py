from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from movies.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'runtime', 'poster', 'detail', 'genre', 'original_language', 'country', 'release_date')
    # movie_director = serializers.IntegerField()
    # movie_actor = serializers.IntegerField()
