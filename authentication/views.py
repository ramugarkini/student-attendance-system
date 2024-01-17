from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from .models import ConfigurationSettings
from .forms import ConfigurationSettingForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.contrib.sites.shortcuts import get_current_site
from functools import wraps

def restrict_access_to_local(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        current_site = get_current_site(request)
        current_site_domain = current_site.domain
        print(get_current_site(request))

        # Check if the current site domain is not '127.0.0.1'
        if current_site_domain != '127.0.0.1:8000':
            # return HttpResponseForbidden("Access Denied")
            return redirect('access_denied')

        return func(request, *args, **kwargs)

    return wrapper


@restrict_access_to_local
def settings(request):
    # Assuming you want to edit the latest ConfigurationSettings object
    setting = ConfigurationSettings.objects.latest('id')

    if request.method == 'POST':
        form = ConfigurationSettingForm(request.POST, request.FILES, instance=setting)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = ConfigurationSettingForm(instance=setting)

    return render(request, 'settings.html', {'form': form})

@restrict_access_to_local
def profile(request):
    # Assuming you want to edit the latest ConfigurationSettings object
    setting = ConfigurationSettings.objects.latest('id')

    if request.method == 'POST':
        form = ConfigurationSettingForm(request.POST, request.FILES, instance=setting)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ConfigurationSettingForm(instance=setting)

    return render(request, 'profile.html', {'form': form})

# do not add restrict_access_to_local
def configuration(request):
    current_site = get_current_site(request)
    current_site_domain = current_site.domain
    is_local = (current_site_domain == '127.0.0.1:8000')

    cs = ConfigurationSettings.objects.latest('id')

    return {'items_per_page': cs.rows_per_page, 'topbar_link': cs.topbar_link, 'topbar_link_text': cs.topbar_link_text, 'sidebar_text': cs.sidebar_text, 'sidebar_icon': cs.sidebar_icon, 'favicon': cs.favicon, 'client_user_name': cs.client_user_name, 'server_user_name': cs.server_user_name, 'user_icon': cs.user_icon, 'is_local': is_local}

@restrict_access_to_local
def allow_access(request):
    setting = ConfigurationSettings.objects.latest('id')

    if request.method == 'POST':
        form = ConfigurationSettingForm(request.POST, request.FILES, instance=setting)
        if form.is_valid():
            form.save()
            return redirect('allow_access')
    else:
        form = ConfigurationSettingForm(instance=setting)

    return render(request, 'allow_access.html', {'form': form})
