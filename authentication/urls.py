# authentication/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('allow_access/', views.allow_access, name='allow_access'),
]