# masters/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('departments/', views.departments, name='departments'),
    path('departments/<int:department_id>/edit/', views.department_edit, name='department_edit'),
    path('api/departments/', views.api_department, name='department_api'),

    path('enrollment_years/', views.enrollment_years, name='enrollment_years'),
    path('enrollment_years/<int:enrollment_year_id>/edit/', views.enrollment_year_edit, name='enrollment_year_edit'),
    path('api/enrollment_years/', views.api_enrollment_year, name='enrollment_year_api'),

    path('academic_years/', views.academic_years, name='academic_years'),
    path('academic_years/<int:academic_year_id>/edit/', views.academic_year_edit, name='academic_year_edit'),
    path('api/academic_years/', views.api_academic_year, name='academic_year_api'),

    path('sections/', views.sections, name='sections'),
    path('sections/<int:section_id>/edit/', views.section_edit, name='section_edit'),
    path('api/sections/', views.api_section, name='section_api'),

    path('subjects/', views.subjects, name='subjects'),
    path('subjects/<int:subject_id>/edit/', views.subject_edit, name='subject_edit'),
    path('api/subjects/', views.api_subject, name='subject_api'),
    
    path('timetables/', views.timetables, name='timetables'),
    path('timetables/<int:timetable_id>/edit/', views.timetable_edit, name='timetable_edit'),

    path('holidays/', views.holidays, name='holidays'),
    path('holidays/<int:holiday_id>/edit/', views.holiday_edit, name='holiday_edit'),

]
