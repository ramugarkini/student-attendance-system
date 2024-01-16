from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse

from django.contrib.sites.shortcuts import get_current_site
from functools import wraps

def restrict_access_to_local(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        current_site = get_current_site(request)
        current_site_domain = current_site.domain

        # Check if the current site domain is not '127.0.0.1'
        if current_site_domain != '127.0.0.1:8000':
            # return HttpResponseForbidden("Access Denied")
            return redirect('access_denied')

        return func(request, *args, **kwargs)

    return wrapper


# @restrict_access_to_local
def index(request):
    return render(request, 'index.html')


def access_denied(request):
    return render(request, 'access_denied.html')
