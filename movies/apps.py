from django.apps import AppConfig


class MoviesConfig(AppConfig):
    name = 'movies'
    verbose_name = 'Django Movie Database'

    def ready(self):
        import movies.signals
