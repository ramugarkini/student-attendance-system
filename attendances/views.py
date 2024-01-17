# attendances/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_GET
from .models import Attendances, AttendanceTimetableDetails, AttendanceTimetableDetailStudents
from .forms import AttendanceForm, AttendanceTimetableDetailForm, AttendanceTimetableDetailStudentForm
from authentication.models import ConfigurationSettings
from django.core.mail import send_mail

from django.contrib import messages
from django.utils import timezone
from datetime import datetime
import pytz

from masters.models import Timetables, TimetableDetails, Departments, EnrollmentYears, Sections
from students.models import Students
import face_recognition
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import os
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from functools import wraps

from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from django.urls import reverse
from django.utils.html import escape
from django.db import IntegrityError

import logging
from django.core.files.base import ContentFile

# Set up logging
logger = logging.getLogger(__name__)


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


def allow_access(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        current_site = get_current_site(request)
        current_site_domain = current_site.domain

        settings = ConfigurationSettings.objects.latest('id')

        if current_site_domain != '127.0.0.1:8000' and settings.allow_access != True:
            # return HttpResponseForbidden("Access Denied")
            return redirect('access_denied')

        return func(request, *args, **kwargs)

    return wrapper

# Create your views here.
@restrict_access_to_local
def attendances(request):
    page = request.GET.get('page', 1)
    search_query = request.GET.get('search', '')
    if search_query:
        all_attendances = Attendances.objects.filter(department__name__icontains=search_query) | Attendances.objects.filter(enrollment_year__year__icontains=search_query).order_by('id')
    else:
        all_attendances = Attendances.objects.all().order_by('id')

    settings = ConfigurationSettings.objects.latest('id')
    items_per_page = settings.rows_per_page
    paginator = Paginator(all_attendances, items_per_page)

    try:
        attendances = paginator.page(page)
    except PageNotAnInteger:
        attendances = paginator.page(1)
    except EmptyPage:
        attendances = paginator.page(paginator.num_pages)

    add_to_loop = ((attendances.number-1)*items_per_page)

    context = {
        'attendances': attendances,
        'search_query': search_query,
        'add_to_loop': add_to_loop
    }

    return render(request, 'attendances.html', context)

@restrict_access_to_local
def attendance_details(request, attendance_id):
   attendance_timetable_details = AttendanceTimetableDetails.objects.filter(attendance_id=attendance_id)

       # Ensure there is at least one instance
   if attendance_timetable_details.exists():
       # Initialize an empty list to store data for each attendance_timetable_detail
       data_list = []

       # Loop through each attendance_timetable_detail
       for detail in attendance_timetable_details:
           # Fetch the related TimetableDetails
           timetable_details = TimetableDetails.objects.filter(id=detail.timetable_detail_id).select_related('subject_detail__subject').first()
           attendance = detail.attendance  # Assuming attendance is the ForeignKey in AttendanceTimetableDetails

           if timetable_details:
               # Extract the required columns for the current detail
               data = {
                   'period_no': timetable_details.period_no,
                   'start_time': timetable_details.start_time,
                   'end_time': timetable_details.end_time,
                   'subject_detail__code': timetable_details.subject_detail.code,
                   'subject_detail__name': timetable_details.subject_detail.name,
                   'attendance_timetable_detail_id': detail.id,
                   'date': attendance.date
               }

               # Append the data to the list
               data_list.append(data)

       # Pass the list of data to the template
       context = {
           'data_list': data_list,
           'attendance_id': attendance_id
       }

   return render(request, 'attendance_details.html', context)


@restrict_access_to_local
def attendance_edit(request, attendance_id):
    attendance = get_object_or_404(Attendances, pk=attendance_id) if attendance_id != 0 else Attendances()
    attendance_timetable_details = attendance.attendancetimetabledetails_set.all() if attendance_id != 0 else None
    # attendance_timetable_details = attendance.attendance_timetable_details.all()

    AttendanceTimetableDetailFormSet = modelformset_factory(
        AttendanceTimetableDetails, 
        form=AttendanceTimetableDetailForm, 
        extra=1, 
        can_delete=True
    )

    if request.method == 'POST':
        if 'delete' in request.POST:
            # Handle delete action
            if attendance:
                attendance.delete()
                return redirect('attendances')  # Redirect after deletion
        else:
            attendance_form = AttendanceForm(request.POST, instance=attendance)
            attendance_timetable_detail_formset = AttendanceTimetableDetailFormSet(
                request.POST, 
                prefix='attendance_timetable_details', 
                queryset=AttendanceTimetableDetails.objects.filter(attendance=attendance)
            )

            if attendance_form.is_valid() and attendance_timetable_detail_formset.is_valid():
                attendance = attendance_form.save()
                messages.success(request, 'Your changes saved successfully.')

                for form in attendance_timetable_detail_formset:
                    if form.cleaned_data.get('DELETE'):
                        form.instance.delete()
                    elif form.cleaned_data:
                        instance = form.save(commit=False)
                        instance.attendance = attendance
                        instance.save()


                return redirect('attendance_edit', attendance_id=attendance.id)
            
    else:
        attendance_form = AttendanceForm(instance=attendance)
        attendance_timetable_detail_formset = AttendanceTimetableDetailFormSet(prefix='attendance_timetable_details', queryset=AttendanceTimetableDetails.objects.filter(attendance=attendance))

    return render(request, 'attendance_edit.html', {'form': attendance_form, 'attendance_timetable_detail_formset': attendance_timetable_detail_formset, 'attendance': attendance})

@restrict_access_to_local
def attendance_detail_edit(request, attendance_id, attendance_timetable_detail_id):
    attendance_timetable_detail = get_object_or_404(AttendanceTimetableDetails, pk=attendance_timetable_detail_id) if attendance_timetable_detail_id != 0 else AttendanceTimetableDetails(attendance_id=attendance_id)
    attendance_timetable_detail_students = attendance_timetable_detail.attendancetimetabledetailstudents_set.all() if attendance_timetable_detail_id != 0 else None
    

    AttendanceTimetableDetailStudentFormSet = modelformset_factory(
        AttendanceTimetableDetailStudents, 
        form=AttendanceTimetableDetailStudentForm, 
        extra=1, 
        can_delete=True
    )

    if request.method == 'POST':
        if 'delete' in request.POST:
            # Handle delete action
            if attendance_timetable_detail:
                attendance_timetable_detail.delete()
                return redirect('attendance_details', attendance_id=attendance_id)  # Redirect after deletion
        else:
            attendance_timetable_detail_form = AttendanceTimetableDetailForm(request.POST, instance=attendance_timetable_detail)
            attendance_timetable_detail_student_formset = AttendanceTimetableDetailStudentFormSet(
                request.POST, 
                prefix='attendance_timetable_detail_students', 
                queryset=AttendanceTimetableDetailStudents.objects.filter(attendance_timetable_detail=attendance_timetable_detail)
            )

            if attendance_timetable_detail_form.is_valid() and attendance_timetable_detail_student_formset.is_valid():
                attendance_timetable_detail = attendance_timetable_detail_form.save()
                messages.success(request, 'Your changes saved successfully.')

                for form in attendance_timetable_detail_student_formset:
                    if form.cleaned_data.get('DELETE'):
                        form.instance.delete()
                    elif form.cleaned_data:
                        instance = form.save(commit=False)
                        instance.attendance_timetable_detail = attendance_timetable_detail
                        instance.save()


                return redirect('attendance_detail_edit', attendance_id=attendance_id, attendance_timetable_detail_id=attendance_timetable_detail.id)
            
    else:
        attendance_timetable_detail_form = AttendanceTimetableDetailForm(instance=attendance_timetable_detail)
        attendance_timetable_detail_student_formset = AttendanceTimetableDetailStudentFormSet(prefix='attendance_timetable_detail_students', queryset=AttendanceTimetableDetailStudents.objects.filter(attendance_timetable_detail=attendance_timetable_detail))

    return render(request, 'attendance_detail_edit.html', {'form': attendance_timetable_detail_form, 'attendance_timetable_detail_student_formset': attendance_timetable_detail_student_formset, 'attendance_timetable_detail': attendance_timetable_detail, 'attendance_id': attendance_id})

#
@allow_access
def face_scan(request):
    current_site = get_current_site(request)
    settings.CSRF_TRUSTED_ORIGINS = [f'https://{current_site.domain}']
    return render(request, 'face_scan.html')

def face_recognize(request):
    if request.method == 'POST':
        try:
            # Decode the base64 image data
            encoded_image_data = request.POST.get('image_data').split(',')[1]
            decoded_image = base64.b64decode(encoded_image_data)

            # Convert the image data to a PIL Image
            pil_image = Image.open(BytesIO(decoded_image))

            # Convert to RGB if the image is in a different mode
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')

            # Perform face recognition
            recognized_face_locations = face_recognition.face_locations(np.array(pil_image))

            logger.info(f"Number of faces detected: {len(recognized_face_locations)}")

            recognized_face_name = None
            student_info = None

            for face_location in recognized_face_locations:
                face_encodings = face_recognition.face_encodings(np.array(pil_image), [face_location])

                if face_encodings:
                    recognized_face_encoding = face_encodings[0]

                    # Load stored face encodings from images in a specific location
                    student_images_path = "media/images/students/"
                    for file_name in os.listdir(student_images_path):
                        if file_name.endswith(".jpg") or file_name.endswith(".jpeg"):
                            file_path = os.path.join(student_images_path, file_name)
                            relative_path = file_path.replace("media/", "")
                            stored_face_image = face_recognition.load_image_file(file_path)
                            stored_face_encoding = face_recognition.face_encodings(stored_face_image)

                            if stored_face_encoding:
                                match = face_recognition.compare_faces([recognized_face_encoding], stored_face_encoding[0])
                                if match and match[0]:
                                    recognized_face_name = os.path.splitext(file_name)[0]

                                    try:
                                        student = Students.objects.get(image=relative_path)
                                        attendance_status = save_attendancetimetabledetail(student.id)

                                        student_info = {
                                            'name': student.name,
                                            'roll_number': student.roll_number,
                                            'department': student.department.name,
                                            'section': student.section.name,
                                            'enrollment_year': student.enrollment_year.year,
                                            'academic_year': student.enrollment_year.academic_year.academic_year,
                                            'image_path': student.image.url,  # Assuming 'image' is the image field in the Student model
                                            'attendance_status': attendance_status,
                                       }
                                    except Students.DoesNotExist:
                                        logger.warning(f"No matching student found in the database for name: {recognized_face_name}")

                                    break

            logger.info(f"Recognized face name: {recognized_face_name}")

            return JsonResponse({'recognized_face_name': recognized_face_name, 'student_info': student_info, 'message': 'Recognition successful'})

        except Exception as e:
            logger.exception("Error processing image data:")
            return JsonResponse({'error': str(e), 'message': 'Error during recognition'}, status=500)

    return JsonResponse({'error': 'Invalid request method', 'message': 'Invalid request method'}, status=400)



def save_attendancetimetabledetail(student_id):
    try:
        # Assuming you have the necessary information for creating attendance records
        student_instance = Students.objects.get(id=student_id)
        department = student_instance.department.id
        enrollment_year = student_instance.enrollment_year.id
        section = student_instance.section.id

        utc_now = datetime.utcnow()
        ist_timezone = pytz.timezone('Asia/Kolkata')
        ist_now = utc_now.replace(tzinfo=pytz.utc).astimezone(ist_timezone)
        ist_weekday = ist_now.isoweekday()

        department_instance = Departments.objects.get(id=department)
        enrollment_year_instance = EnrollmentYears.objects.get(id=enrollment_year)
        section_instance = Sections.objects.get(id=section)
        timetable_instance  = Timetables.objects.filter(
            department_id=department,
            weekday=ist_weekday,
            enrollment_year_id=enrollment_year,
            section_id=section
        ).order_by('-id').first()


        result_message = ""

        if timetable_instance:
            result_message = f"Timetable found!"
            # Get the current date and time in IST
            ist_now = timezone.now().astimezone(pytz.timezone('Asia/Kolkata'))
            ist_date = ist_now.date()
            ist_time = ist_now.time()

            # Check if an entry with the specified date and timetable exists
            existing_attendance = Attendances.objects.filter(
                date=ist_date,
                timetable=timetable_instance
            ).first()

            if existing_attendance:
                # Entry with the specified date and timetable already exists
                attendance_instance = existing_attendance
            else:
                # Entry does not exist, create a new one
                new_attendance = Attendances.objects.create(
                    date=ist_date,
                    weekday=ist_weekday,
                    department=department_instance,
                    enrollment_year=enrollment_year_instance,
                    section=section_instance,
                    timetable=timetable_instance,
                )
                attendance_instance = new_attendance

            timetable_detail_instance = TimetableDetails.objects.filter(
                timetable=timetable_instance,
                start_time__lte=ist_now.time(),  # Check if ist_now.time() is after or equal to start_time
                end_time__gte=ist_now.time(),    # Check if ist_now.time() is before or equal to end_time
            ).first()

            # result_message = ""

            if timetable_detail_instance:
                # Access the associated SubjectDetails and retrieve the code
                subject_detail_name = timetable_detail_instance.subject_detail.name

                existing_attendance_timetabledetail = AttendanceTimetableDetails.objects.filter(
                    attendance=attendance_instance,
                    # student=student_instance,
                    timetable_detail=timetable_detail_instance,
                ).first()

                if existing_attendance_timetabledetail:
                    attendance_timetabledetail_instance = existing_attendance_timetabledetail
                else:
                    new_attendance_timetabledetail = AttendanceTimetableDetails.objects.create(
                        attendance=attendance_instance,
                        timetable_detail=timetable_detail_instance,
                    )
                    attendance_timetabledetail_instance = new_attendance_timetabledetail

                # 
                existing_attendancetabledetail_student = AttendanceTimetableDetailStudents.objects.filter(
                    student=student_instance,
                    attendance_timetable_detail=attendance_timetabledetail_instance,
                ).first()

                if existing_attendancetabledetail_student:
                    attendancetabledetail_student_instance = existing_attendancetabledetail_student
                    return f"Existing attendance. Date and Time: {attendancetabledetail_student_instance.date.strftime('%d-%m-%Y')} {attendancetabledetail_student_instance.time.strftime('%H:%M:%S')}. Subject: {subject_detail_name}"

                else:
                    new_attendancetabledetail_student = AttendanceTimetableDetailStudents.objects.create(
                        attendance_timetable_detail=attendance_timetabledetail_instance,
                        student=student_instance,
                        date=ist_date,
                        time=ist_time,
                        attendance_type=2,  # Assuming 2 represents face scan attendance
                    )
                    attendancetabledetail_student_instance = new_attendancetabledetail_student

                    send_email(student_id, subject_detail_name, attendancetabledetail_student_instance.date.strftime('%d-%m-%Y'), attendancetabledetail_student_instance.time.strftime('%H:%M:%S'))
                    
                    return f"Your attendance has been saved successfully. Date and Time: {attendancetabledetail_student_instance.date.strftime('%d-%m-%Y')} {attendancetabledetail_student_instance.time.strftime('%H:%M:%S')}. Subject: {subject_detail_name}"
            else:
                return "No matching Timetable Details for the Current time"
        else:
            # Timetable detail instance not found
            result_message = "Timetable not created"
            
            return result_message  # Indicate success if needed

    except Exception as e:
        # Log the error or handle it appropriately
        print(f"Error saving attendance: {e}")
        return False  # Indicate failure if needed

def send_email(student_id, subject_detail_name, attendance_date, attendance_time):
    try:
        student_instance = Students.objects.get(id=student_id)

        subject = 'Face Scan Attendance Notification'
        message = f"""
Dear {student_instance.name},

This is to inform you that your attendance has been successfully recorded through a face scan.

Details:
- Student Name: {student_instance.name}
- Roll No: {student_instance.roll_number}
- Class: {subject_detail_name}
- Date and Time: {attendance_date} {attendance_time}

If you believe this is an error or if you have any concerns regarding your attendance, please contact your Class Representative.

This is a system-generated email. Please do not reply.
"""
        recipient_list = [student_instance.email]
        # recipient_list = ['ramuasece@gmail.com']
        # cc_list = ['ramu.garkini@gmail.com']

        # Customize the sender email and other parameters as needed
        sender_email = 'noreply.322136410122@gmail.com'

        send_mail(
            subject,
            message,
            sender_email,
            recipient_list,
            cc=cc_list,
            fail_silently=False,  # Set to True to suppress exceptions (useful during development)
        )

        return JsonResponse({'message': 'Email sent successfully'})
    except Exception as e:
        # Catching other exceptions and returning an error JSON response
        return JsonResponse({'error': str(e)}, status=500)

# API for saving attendance based on student id
# not in use
@require_GET
def api_attendance(request):
    student_id = request.GET.get('student')

    if student_id is not None:
        try:
            # Convert the student_id to an integer
            student_id = int(student_id)

            # Retrieve the student instance
            student = Students.objects.get(id=student_id)
            
            # Your logic to save attendance based on the student instance
            # ...

            # You can return any response you want
            return JsonResponse({'message': 'Attendance saved successfully'})
        except Students.DoesNotExist:
            return JsonResponse({'error': 'Invalid student ID or student not found'}, status=400)
    else:
        return JsonResponse({'error': 'Missing student_id parameter'}, status=400)

# not in use
@require_GET
def api_send_email(request):
    try:
        """
        Send a custom email using Django's send_mail function.

        Parameters:
        - subject: The subject of the email.
        - message: The body of the email.
        - recipient_list: List of recipient email addresses.
        """
        subject = 'Hello from Django!'
        message = 'This is a test email sent from a Django app.'
        recipient_list = ['ramuasece@gmail.com']

        # Customize the sender email and other parameters as needed
        sender_email = 'noreply.322136410122@gmail.com'

        send_mail(
            subject,
            message,
            sender_email,
            recipient_list,
            fail_silently=False,  # Set to True to suppress exceptions (useful during development)
        )

        return JsonResponse({'message': 'Email sent successfully'})
    except Exception as e:
        # Catching other exceptions and returning an error JSON response
        return JsonResponse({'error': str(e)}, status=500)



@restrict_access_to_local
def attendances_report(request):
    page = request.GET.get('page', 1)
    all_attendances = Attendances.objects.all()

    settings = ConfigurationSettings.objects.latest('id')
    items_per_page = settings.rows_per_page
    paginator = Paginator(all_attendances, items_per_page)

    try:
        attendances = paginator.page(page)
    except PageNotAnInteger:
        attendances = paginator.page(1)
    except EmptyPage:
        attendances = paginator.page(paginator.num_pages)

    add_to_loop = ((attendances.number-1)*items_per_page)

    context = {
        'attendances': attendances,
        'add_to_loop': add_to_loop
    }

    return render(request, 'attendances_report.html', context)

@restrict_access_to_local
def attendance_details_report(request, attendance_id):
   attendance_timetable_details = AttendanceTimetableDetails.objects.filter(attendance_id=attendance_id)

       # Ensure there is at least one instance
   if attendance_timetable_details.exists():
       # Initialize an empty list to store data for each attendance_timetable_detail
       data_list = []

       # Loop through each attendance_timetable_detail
       for detail in attendance_timetable_details:
           # Fetch the related TimetableDetails
           timetable_details = TimetableDetails.objects.filter(id=detail.timetable_detail_id).select_related('subject_detail__subject').first()
           attendance = detail.attendance

           if timetable_details:
               # Extract the required columns for the current detail
               data = {
                   'period_no': timetable_details.period_no,
                   'start_time': timetable_details.start_time,
                   'end_time': timetable_details.end_time,
                   'subject_detail__code': timetable_details.subject_detail.code,
                   'subject_detail__name': timetable_details.subject_detail.name,
                   'attendance_timetable_detail_id': detail.id,
                   'date': attendance.date
               }

               # Append the data to the list
               data_list.append(data)

       # Pass the list of data to the template
       context = {
           'data_list': data_list,
           'attendance_id': attendance_id
       }

   return render(request, 'attendance_details_report.html', context)

def students_report(request, attendance_id, attendance_timetable_detail_id, pdf=0):
    attendance_timetable_detail_students = AttendanceTimetableDetailStudents.objects.filter(attendance_timetable_detail_id=attendance_timetable_detail_id)

    # Extracting student details for each attendance detail
    student_attendance_details = [
        {
            'date': detail.date,
            'time': detail.time,
            'student_id': detail.student.id,
            'student_name': detail.student.name,
            'roll_number': detail.student.roll_number,
        }
        for detail in attendance_timetable_detail_students
    ]

    attendance_timetable_detail = get_object_or_404(AttendanceTimetableDetails, id=attendance_timetable_detail_id)

    attendance = get_object_or_404(Attendances, id=attendance_id)

    # Extract information from the attendance object
    date = attendance.date
    weekday = attendance.get_weekday_display()
    department = attendance.department.name
    enrollment_year = attendance.enrollment_year.academic_year.academic_year
    section = attendance.section.name
        
    # Extracting relevant details from the first attendance_detail assuming all details share the same date, time, and timetable
    if attendance_timetable_detail:
        timetable_details = attendance_timetable_detail.timetable_detail
        period_no = timetable_details.period_no
        start_time = timetable_details.start_time
        end_time = timetable_details.end_time
        subject_code = timetable_details.subject_detail.code
        subject_name = timetable_details.subject_detail.name

        # Fetching student attendance details
        student_details = Students.objects.filter(
            department_id=attendance.department.id,
            enrollment_year_id=attendance.enrollment_year.id,
            section_id=attendance.section.id
        )

        for student in student_details:
            attendance_detail = next((detail for detail in student_attendance_details if detail['student_id'] == student.id), None)
            if attendance_detail:
                student.attendance_status = 'Present'
                student.date = attendance_detail['date']
                student.time = attendance_detail['time']
                student.student_name = attendance_detail['student_name']
                student.roll_number = attendance_detail['roll_number']
            else:
                student.attendance_status = 'Absent'
                student.date = '-'
                student.time = '-'
                student.student_name = student.name
                student.roll_number = student.roll_number

        context = {
            'date': date,
            'period_no': period_no,
            'start_time': start_time,
            'end_time': end_time,
            'department': department,
            'section': section,
            'enrollment_year': enrollment_year,
            'weekday': weekday,
            'subject_code': subject_code,
            'subject_name': subject_name,
            'student_details': student_details,
            'attendance_id': attendance_id,
            'attendance_timetable_detail_id': attendance_timetable_detail_id
        }

        if (pdf == 1):
            template_path = 'students_pdf.html'
            return render_to_pdf(template_path, context)
        else:
            return render(request, 'students_report.html', context)

def render_to_pdf(template_path, context_dict):
    template = get_template(template_path)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    formatted_date = context_dict['date'].strftime("%d_%m_%Y")
    pdf_filename = (
        formatted_date + ' '
        + context_dict['department'] + ' '
        + context_dict['section'] + ' '
        + context_dict['enrollment_year'] + ' '
        + context_dict['subject_code'] + ' '
        + "Attendance"
    )

    response['Content-Disposition'] = f'filename="{pdf_filename}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + escape(html) + '</pre>')
    return response
