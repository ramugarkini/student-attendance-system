# students/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('students/', views.students, name='students'),
    path('students/<int:student_id>/edit/', views.student_edit, name='student_edit'),
    path('scan_face/', views.scan_face, name='scan_face'),
    path('recognize_face/', views.recognize_face, name='recognize_face'),
]
