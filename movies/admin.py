from django.contrib import admin
from movies.models import Movie, MovieActor, MovieDirector, MovieRate


class MovieAdmin(admin.ModelAdmin):
    pass


class MovieRateAdmin(admin.ModelAdmin):
    pass


class MovieDirectorAdmin(admin.ModelAdmin):
    pass


class MovieActorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieRate, MovieRateAdmin)
admin.site.register(MovieDirector, MovieDirectorAdmin)
admin.site.register(MovieActor, MovieActorAdmin)
