from django.conf import settings
from django.contrib import auth
from datetime import datetime, timedelta, tzinfo, timezone

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from movies.models import UserUniqueToken


class AutoLogoutMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                dt = request.user.last_login - timedelta(hours=5)
                naive = dt.replace(tzinfo=None)  # Delete timezone
                print(naive)
                if datetime.now() - naive > timedelta(hours=2):
                    UserUniqueToken.objects.get(user_id=request.user.pk).delete()
                    auth.logout(request)
                    print('Logged Out')
                    return redirect('movies:login')
            except TypeError:
                print('Error')
                pass

        elif request.META['PATH_INFO'] != '/':
            return redirect('movies:login')
