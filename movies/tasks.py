from movie_project.local_settings import HideSettingsEmail
from celery._state import get_current_app
from django.core.mail import send_mail

from django.core.management import call_command

app = get_current_app()


@app.task()
def download_task(option, movie_name):
    print('in celery module')
    movies = call_command('download', option, movie_name)
    send_email(movies)


@app.task()
def send_email(movies):
    if len(movies) > 11:
        print(f'Sending email to {HideSettingsEmail.to}')
        send_mail(
            'Downloaded Movies',
            movies,
            HideSettingsEmail.email,
            [HideSettingsEmail.to],
        )
    else:
        print('Email not sent')
