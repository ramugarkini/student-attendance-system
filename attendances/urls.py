# students/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('attendances/', views.attendances, name='attendances'),
    path('attendance_details/<int:attendance_id>/', views.attendance_details, name='attendance_details'),
    path('attendances/<int:attendance_id>/edit/', views.attendance_edit, name='attendance_edit'),

    path('attendance_details/<int:attendance_id>/<int:attendance_timetable_detail_id>/edit/', views.attendance_detail_edit, name='attendance_detail_edit'),

    path('face_scan/', views.face_scan, name='face_scan'),
    path('face_recognize/', views.face_recognize, name='face_recognize'),

    path('api/attendances/', views.api_attendance, name='attendance_api'),
    path('api/send_emails/', views.api_send_email, name='send_email_api'),
    
    path('attendances_report/', views.attendances_report, name='attendances_report'),
    path('attendance_details_report/<int:attendance_id>/', views.attendance_details_report, name='attendance_details_report'),
    path('students_report/<int:attendance_id>/<int:attendance_timetable_detail_id>/<int:pdf>', views.students_report, name='students_report'),
]
