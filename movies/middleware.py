from django.conf import settings
from django.contrib import auth
from datetime import datetime, timedelta, tzinfo

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
                dt = request.user.last_login
                naive = dt.replace(tzinfo=None)  # Delete timezone
                if datetime.now() - naive > timedelta(hours=1):
                    UserUniqueToken.objects.get(user_id=request.user.pk).delete()
                    auth.logout(request)
                    response = datetime.now()
                    return response
            except TypeError:
                print('Error')
                pass
        elif request.META['PATH_INFO'] != '/':
            return redirect('movies:login')
