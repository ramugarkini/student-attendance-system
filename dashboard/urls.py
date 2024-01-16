# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('access_denied/', views.access_denied, name='access_denied'),
]
