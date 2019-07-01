import os

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from movies.models import Movie, MovieDirector, MovieActor
from django.core.files import File
import re


def valid_poster(i):

    path_poster = ''

    movie_id = i['imdbID']
    response_id = requests.get("http://www.omdbapi.com/?i=" + movie_id + "&plot=full&apikey=ee45eeb2")
    r_id = response_id.json()

    poster, title = r_id['Poster'], r_id['Title']
    if poster != "N/A":
        # title_ = ''.join(title.split('/'))
        title_ = re.sub('[^a-zA-Z0-9]', '', title)
        path_image = '/movie/' + title_ + '/'
        ext = poster[-3:]

        # Create target directory & all intermediate directories if don't exists
        if not os.path.exists(settings.MEDIA_ROOT + path_image):
            os.makedirs(settings.MEDIA_ROOT + path_image)
            print("Directory ", settings.MEDIA_ROOT + path_image, " Created ")

            resp = requests.get(poster)
            my_file = File(open(settings.MEDIA_ROOT + path_image + 'poster' + title_ + '.' + ext, 'wb'))
            my_file.name = 'poster' + title_ + '.' + ext
            my_file.write(resp.content)
            my_file.close()
            path_poster = path_image[1:] + my_file.name

        else:
            print("Directory ", settings.MEDIA_ROOT + path_image, " already exists")

    else:
        print(f'Ignored Movie "{title}", without poster!')

    return r_id, path_poster


def create_movie(r_id, path_poster, movie_list):
    director, _ = MovieDirector.objects.get_or_create(name=r_id['Director'].split(', ')[0])
    actors, _ = MovieActor.objects.get_or_create(name=r_id['Actors'])

    m, _ = Movie.objects.get_or_create(title=r_id['Title'], runtime=r_id['Runtime'], poster=path_poster,
                                       detail=r_id['Plot'], genre=r_id['Genre'].split(', ')[0],
                                       original_language=r_id['Language'].split(', ')[0],
                                       country=r_id['Country'].split(', ')[0])

    m.movie_director.add(director)
    m.movie_actor.add(actors)
    movie_list += r_id['Title'] + '\n'
    return movie_list


class Command(BaseCommand):
    help = 'fetch movies from OMDB API'

    def add_arguments(self, parser):
        # positional argument
        parser.add_argument('title', type=str)

        # kwargs like arguments
        parser.add_argument('-s', '--search', action='store_true', default=False)
        parser.add_argument('-t', '--title_', action='store_true', default=False)

    def handle(self, *args, **options):
        search = options['search']
        title = options['title']
        movie_list = 'Movie(s): \n'

        if options['search']:
            response = requests.get("http://www.omdbapi.com/?s=" + title + "&plot=full&apikey=ee45eeb2")
            r = response.json()
            for i in r['Search']:
                r_id, path_poster = valid_poster(i)
                if path_poster != '':
                    movie_list = create_movie(r_id, path_poster, movie_list)

            return movie_list

        elif options['title_']:
            response = requests.get('http://www.omdbapi.com/?t=' + title + '&plot=full&apikey=ee45eeb2')
            r = response.json()

            r_id, path_poster = valid_poster(r)
            if path_poster != '':
                movie_list = create_movie(r_id, path_poster, movie_list)

            return movie_list

        else:
            print("Error: option is not valid")

