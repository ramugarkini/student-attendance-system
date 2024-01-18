# students/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Students
from .forms import StudentForm
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
import face_recognition
import numpy as np
import base64
from io import BytesIO
from PIL import Image
import os
from django.conf import settings
from authentication.models import ConfigurationSettings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from functools import wraps

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
        if current_site_domain != '127.0.0.1':
            # return HttpResponseForbidden("Access Denied")
            return redirect('access_denied')

        return func(request, *args, **kwargs)

    return wrapper

# def index(request):
#     return render(request, 'index.html') 

@restrict_access_to_local
def students(request):
    page = request.GET.get('page', 1)
    search_query = request.GET.get('search', '')
    if search_query:
        all_students = Students.objects.filter(name__icontains=search_query) | Students.objects.filter(roll_number__icontains=search_query) | Students.objects.filter(department__name__icontains=search_query) | Students.objects.filter(enrollment_year__year__icontains=search_query)
    else:
        all_students = Students.objects.all()

    settings = ConfigurationSettings.objects.latest('id')
    items_per_page = settings.rows_per_page
    paginator = Paginator(all_students, items_per_page)

    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    add_to_loop = ((students.number-1)*items_per_page)

    context = {
        'students': students,
        'search_query': search_query,
        'add_to_loop': add_to_loop
    }

    return render(request, 'students.html', context)

@restrict_access_to_local
def student_edit(request, student_id):
    if student_id == 0:
        student = Students()  # For a new student instance
    else:
        student = get_object_or_404(Students, pk=student_id)

    if request.method == 'POST':
        if 'delete' in request.POST:
            # Handle delete action
            if student:
                student.delete()
                return redirect('students')  # Redirect after deletion
        else:
            form = StudentForm(request.POST, request.FILES, instance=student)
            if form.is_valid():
                student = form.save(commit=False)

                
                # Process captured image if available
                if 'image_data' in request.POST:
                    if request.POST.get('remove_image_data'):
                        # Clear the existing image
                        student.image.delete()

                        # Save the student instance after deleting the image
                        student.save()

                        # Remove the image file from the local file system
                        if student.image:
                            image_path = student.image.path
                            if os.path.exists(image_path):
                                os.remove(image_path)

                    image_data_parts = request.POST.get('image_data').split(';base64,')

                    # Check if the split result has two elements
                    if len(image_data_parts) == 2:
                        format, imgstr = image_data_parts
                        # Create a unique filename based on student name and roll number
                        filename = f"{student.name}_{student.roll_number}.{format.split('/')[-1]}"
                        
                        # Decode the image data
                        img_data = base64.b64decode(imgstr)

                        # Save the image to the student instance with the specified filename
                        student.image.save(filename, ContentFile(img_data, name=filename), save=False)
                    else:
                        # Handle the case where the split result doesn't have two elements
                        # You might want to log a warning or handle this situation according to your needs
                        print("Unexpected format for image_data:", request.POST.get('image_data'))

                # Save the student instance
                student.save()
                messages.success(request, 'Your changes saved successfully.')

                return redirect('student_edit', student_id=student.id)

    else:
        form = StudentForm(instance=student)

    return render(request, 'student_edit.html', {'form': form, 'student': student})

# def encode_face(image_path):
#     # Load the image and encode the face
#     image = face_recognition.load_image_file(image_path)
    
#     # Check if any faces are found
#     face_encodings = face_recognition.face_encodings(image)
#     if not face_encodings:
#         # Handle the case where no faces are detected
#         return None
    
#     # Return the face encoding of the first face
#     return face_encodings[0]

@csrf_exempt
def scan_face(request):
    # Your view logic for the scan_face page
    current_site = get_current_site(request)
    settings.CSRF_TRUSTED_ORIGINS = [f'https://{current_site.domain}']
    return render(request, 'scan_face.html')

@csrf_exempt
def recognize_face(request):
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
                                        print(relative_path)
                                        student = Students.objects.get(image=relative_path)

                                        student_info = {
                                            'name': student.name,
                                            'roll_number': student.roll_number,
                                            'department': student.department.name,
                                            'section': student.section.name,
                                            'enrollment_year': student.enrollment_year.year,
                                            'academic_year': student.enrollment_year.academic_year.academic_year,
                                            'image_path': student.image.url,  # Assuming 'image' is the image field in the Student model
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

