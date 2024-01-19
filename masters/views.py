# masters/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_GET
from django.contrib import messages
from .models import Departments, EnrollmentYears, AcademicYears, Sections, Subjects, SubjectDetails, Timetables, TimetableDetails, Holidays, HolidayDetails
from .forms import DepartmentForm, EnrollmentYearForm, AcademicYearForm, SectionForm, SubjectForm, SubjectDetailForm, TimetableForm, TimetableDetailForm, HolidayForm, HolidayDetailForm
from authentication.models import ConfigurationSettings

from django.contrib.sites.shortcuts import get_current_site
from functools import wraps


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

# def departments(request):
    # departments = Departments.objects.all()
    # return render(request, 'departments.html', {'departments': departments})

@restrict_access_to_local
def departments(request):
    # Assuming 'page' is the query parameter for page number
    page = request.GET.get('page', 1)

    # Fetch all departments or filter by search query
    search_query = request.GET.get('search', '')
    if search_query:
        all_departments = Departments.objects.filter(name__icontains=search_query) | Departments.objects.filter(code__icontains=search_query).order_by('code')
    else:
        all_departments = Departments.objects.all().order_by('code')

    # Set the number of items per page
    settings = ConfigurationSettings.objects.latest('id')
    items_per_page = settings.rows_per_page
    paginator = Paginator(all_departments, items_per_page)

    try:
        departments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        departments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page
        departments = paginator.page(paginator.num_pages)

    add_to_loop = ((departments.number-1)*items_per_page)

    context = {
        'departments': departments,
        'search_query': search_query,
        'add_to_loop': add_to_loop
    }

    return render(request, 'departments.html', context)

@restrict_access_to_local
def department_edit(request, department_id):
    department = get_object_or_404(Departments, pk=department_id) if department_id != 0 else Departments()

    if request.method == 'POST':
        if 'delete' in request.POST:
            # Handle delete action
            if department:
                department.delete()
                return redirect('departments')  # Redirect after deletion
        else:
            form = DepartmentForm(request.POST, instance=department)
            if form.is_valid():
                department = form.save()
                messages.success(request, 'Your changes saved successfully.')
                return redirect('department_edit', department_id=department.id)

    else:
        form = DepartmentForm(instance=department)

    return render(request, 'department_edit.html', {'form': form, 'department': department})

@restrict_access_to_local
def api_department(request):
    departments = Departments.objects.values('id', 'code', 'name')
    data = list(departments)
    # departments = Department.objects.all()
    # data = [{'id': department.id, 'code': department.code, 'name': department.name} for department in departments]
    return JsonResponse(data, safe=False)


@restrict_access_to_local
def enrollment_years(request):
    page = request.GET.get('page', 1)
    search_query = request.GET.get('search', '')
    if search_query:
        all_enrollment_years = EnrollmentYears.objects.filter(code__icontains=search_query) | EnrollmentYears.objects.filter(year__icontains=search_query)
    else:
        all_enrollment_years = EnrollmentYears.objects.all().order_by('-year')  # Order by year in descending order

    settings = ConfigurationSettings.objects.latest('id')
    items_per_page = settings.rows_per_page
    paginator = Paginator(all_enrollment_years, items_per_page)

    try:
        enrollment_years = paginator.page(page)
    except PageNotAnInteger:
        enrollment_years = paginator.page(1)
    except EmptyPage:
        enrollment_years = paginator.page(paginator.num_pages)

    add_to_loop = ((enrollment_years.number-1)*items_per_page)

    context = {
        'enrollment_years': enrollment_years,
        'search_query': search_query,
        'add_to_loop': add_to_loop
    }

    return render(request, 'enrollment_years.html', context)

@restrict_access_to_local
def enrollment_year_edit(request, enrollment_year_id):
    enrollment_year = get_object_or_404(EnrollmentYears, pk=enrollment_year_id) if enrollment_year_id != 0 else EnrollmentYears()

    if request.method == 'POST':
        if 'delete' in request.POST:
            # Handle delete action
            if enrollment_year:
                enrollment_year.delete()
                return redirect('enrollment_years')  # Redirect after deletion
        else:
            form = EnrollmentYearForm(request.POST, instance=enrollment_year)
            if form.is_valid():
                enrollment_year = form.save()
                messages.success(request, 'Your changes saved successfully.')
                return redirect('enrollment_year_edit', enrollment_year_id=enrollment_year.id)

    else:
        form = EnrollmentYearForm(instance=enrollment_year)

    return render(request, 'enrollment_year_edit.html', {'form': form, 'enrollment_year': enrollment_year})

@restrict_access_to_local
def api_enrollment_year(request):
    enrollment_years = EnrollmentYears.objects.values('id', 'code', 'year')
    data = list(enrollment_years)
    return JsonResponse(data, safe=False)


@restrict_access_to_local
def academic_years(request):
    page = request.GET.get('page', 1)
    search_query = request.GET.get('search', '')
    if search_query:
        all_academic_years = AcademicYears.objects.filter(academic_year__icontains=search_query).order_by('academic_year')
    else:
        all_academic_years = AcademicYears.objects.all().order_by('academic_year')  # Order by year in descending order

    settings = ConfigurationSettings.objects.latest('id')
    items_per_page = settings.rows_per_page
    paginator = Paginator(all_academic_years, items_per_page)

    try:
        academic_years = paginator.page(page)
    except PageNotAnInteger:
        academic_years = paginator.page(1)
    except EmptyPage:
        academic_years = paginator.page(paginator.num_pages)

    add_to_loop = ((academic_years.number-1)*items_per_page)

    context = {
        'academic_years': academic_years,
        'search_query': search_query,
        'add_to_loop': add_to_loop
    }

    return render(request, 'academic_years.html', context)

@restrict_access_to_local
def academic_year_edit(request, academic_year_id):
    academic_year = get_object_or_404(AcademicYears, pk=academic_year_id) if academic_year_id != 0 else AcademicYears()

    if request.method == 'POST':
        if 'delete' in request.POST:
            # Handle delete action
            if academic_year:
                academic_year.delete()
                return redirect('academic_years')  # Redirect after deletion
        else:
            form = AcademicYearForm(request.POST, instance=academic_year)
            if form.is_valid():
                academic_year = form.save()
                messages.success(request, 'Your changes saved successfully.')
                return redirect('academic_year_edit', academic_year_id=academic_year.id)

    else:
        form = AcademicYearForm(instance=academic_year)

    return render(request, 'academic_year_edit.html', {'form': form, 'academic_year': academic_year})

@restrict_access_to_local
def api_academic_year(request):
    academic_years = AcademicYears.objects.values('id', 'year')
    data = list(academic_years)
    return JsonResponse(data, safe=False)


@restrict_access_to_local
def sections(request):
    page = request.GET.get('page', 1)

    search_query = request.GET.get('search', '')
    if search_query:
        all_sections = Sections.objects.filter(name__icontains=search_query).order_by('name')
    else:
        all_sections = Sections.objects.all().order_by('name')

    settings = ConfigurationSettings.objects.latest('id')
    items_per_page = settings.rows_per_page
    paginator = Paginator(all_sections, items_per_page)

    try:
        sections = paginator.page(page)
    except PageNotAnInteger:
        sections = paginator.page(1)
    except EmptyPage:
        sections = paginator.page(paginator.num_pages)

    add_to_loop = ((sections.number-1)*items_per_page)

    context = {
        'sections': sections,
        'search_query': search_query,
        'add_to_loop': add_to_loop
    }

    return render(request, 'sections.html', context)

@restrict_access_to_local
def section_edit(request, section_id):
    section = get_object_or_404(Sections, pk=section_id) if section_id != 0 else Sections()

    if request.method == 'POST':
        if 'delete' in request.POST:
            # Handle delete action
            if section:
                section.delete()
                return redirect('sections')  # Redirect after deletion
        else:
            form = SectionForm(request.POST, instance=section)
            if form.is_valid():
                section = form.save()
                messages.success(request, 'Your changes saved successfully.')
                return redirect('section_edit', section_id=section.id)

    else:
        form = SectionForm(instance=section)

    return render(request, 'section_edit.html', {'form': form, 'section': section})

@restrict_access_to_local
def api_section(request):
    sections = Sections.objects.values('id', 'name')
    data = list(sections)
    return JsonResponse(data, safe=False)


@restrict_access_to_local
def subjects(request):
    page = request.GET.get('page', 1)
    search_query = request.GET.get('search', '')
    if search_query:
        all_subjects = Subjects.objects.filter(department__name__icontains=search_query) | Subjects.objects.filter(academic_year__academic_year__icontains=search_query).order_by('academic_year__academic_year')
    else:
        all_subjects = Subjects.objects.all().order_by('academic_year__academic_year')

    subjects_with_count = []

    for subject in all_subjects:
        count_of_details = SubjectDetails.objects.filter(subject=subject).count()
        subjects_with_count.append((subject, count_of_details))

    settings = ConfigurationSettings.objects.latest('id')
    items_per_page = settings.rows_per_page
    paginator = Paginator(all_subjects, items_per_page)

    try:
        subjects = paginator.page(page)
    except PageNotAnInteger:
        subjects = paginator.page(1)
    except EmptyPage:
        subjects = paginator.page(paginator.num_pages)

    add_to_loop = ((subjects.number-1)*items_per_page)

    context = {
        'subjects': subjects,
        'subjects_with_count': subjects_with_count,
        'search_query': search_query,
        'add_to_loop': add_to_loop
    }

    return render(request, 'subjects.html', context)

@restrict_access_to_local
def subject_edit(request, subject_id):
    subject = get_object_or_404(Subjects, pk=subject_id) if subject_id != 0 else Subjects()
    subject_details = subject.subjectdetails_set.all() if subject_id != 0 else None
    # subject_details = subject.subject_details.all()

    SubjectDetailFormSet = modelformset_factory(
        SubjectDetails, 
        form=SubjectDetailForm, 
        extra=1, 
        can_delete=True
    )

    if request.method == 'POST':
        if 'delete' in request.POST:
            # Handle delete action
            if subject:
                subject.delete()
                return redirect('subjects')  # Redirect after deletion
        else:
            subject_form = SubjectForm(request.POST, instance=subject)
            subject_detail_formset = SubjectDetailFormSet(
                request.POST, 
                prefix='subject_details', 
                queryset=SubjectDetails.objects.filter(subject=subject)
            )

            if subject_form.is_valid() and subject_detail_formset.is_valid():
                subject = subject_form.save()
                messages.success(request, 'Your changes saved successfully.')

                for form in subject_detail_formset:
                    if form.cleaned_data.get('DELETE'):
                        form.instance.delete()
                    elif form.cleaned_data:
                        instance = form.save(commit=False)
                        instance.subject = subject
                        instance.save()


                return redirect('subject_edit', subject_id=subject.id)
            
    else:
        subject_form = SubjectForm(instance=subject)
        subject_detail_formset = SubjectDetailFormSet(prefix='subject_details', queryset=SubjectDetails.objects.filter(subject=subject))

    return render(request, 'subject_edit.html', {'form': subject_form, 'subject_detail_formset': subject_detail_formset, 'subject': subject})

@require_GET
def api_subject(request):
    department_id = request.GET.get('department')
    enrollment_year_id = request.GET.get('enrollment_year')

    try:
        enrollment_years_instance = EnrollmentYears.objects.get(id=enrollment_year_id)
        academic_year_id = enrollment_years_instance.academic_year_id
    except EnrollmentYears.DoesNotExist:
        return JsonResponse({'error': 'Invalid enrollment year ID'}, status=400)

    if department_id and academic_year_id:
        # Filter subjects based on department, academic_year
        subjects = SubjectDetails.objects.filter(
            subject__department_id=department_id,
            subject__academic_year_id=academic_year_id
        )

        subjects_data = [{'id': subject.id, 'name': subject.name} for subject in subjects]
        return JsonResponse(subjects_data, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@restrict_access_to_local
def timetables(request):
    page = request.GET.get('page', 1)
    search_query = request.GET.get('search', '')
    if search_query:
        all_timetables = Timetables.objects.filter(department__name__icontains=search_query) | Timetables.objects.filter(enrollment_year__year__icontains=search_query).order_by('enrollment_year__academic_year__academic_year')
    else:
        all_timetables = Timetables.objects.all().order_by('enrollment_year__academic_year__academic_year')

    settings = ConfigurationSettings.objects.latest('id')
    items_per_page = settings.rows_per_page
    paginator = Paginator(all_timetables, items_per_page)

    try:
        timetables = paginator.page(page)
    except PageNotAnInteger:
        timetables = paginator.page(1)
    except EmptyPage:
        timetables = paginator.page(paginator.num_pages)

    add_to_loop = ((timetables.number-1)*items_per_page)

    context = {
        'timetables': timetables,
        'search_query': search_query,
        'add_to_loop': add_to_loop
    }

    return render(request, 'timetables.html', context)

@restrict_access_to_local
def timetable_edit(request, timetable_id):
    timetable = get_object_or_404(Timetables, pk=timetable_id) if timetable_id != 0 else Timetables()
    timetable_details = timetable.timetabledetails_set.all() if timetable_id != 0 else None

    TimetableDetailFormSet = modelformset_factory(
        TimetableDetails, 
        form=TimetableDetailForm, 
        extra=1, 
        can_delete=True
    )

    if request.method == 'POST':
        if 'delete' in request.POST:
            # Handle delete action
            if timetable:
                timetable.delete()
                return redirect('timetables')  # Redirect after deletion
        else:
            timetable_form = TimetableForm(request.POST, instance=timetable)
            timetable_detail_formset = TimetableDetailFormSet(
                request.POST, 
                prefix='timetable_details', 
                queryset=TimetableDetails.objects.filter(timetable=timetable)
            )

            if timetable_form.is_valid() and timetable_detail_formset.is_valid():
                timetable = timetable_form.save()
                messages.success(request, 'Your changes saved successfully.')

                for form in timetable_detail_formset:
                    if form.cleaned_data.get('DELETE'):
                        form.instance.delete()
                    elif form.cleaned_data:
                        instance = form.save(commit=False)
                        instance.timetable = timetable
                        instance.save()


                return redirect('timetable_edit', timetable_id=timetable.id)
            
    else:
        timetable_form = TimetableForm(instance=timetable)
        timetable_detail_formset = TimetableDetailFormSet(prefix='timetable_details', queryset=TimetableDetails.objects.filter(timetable=timetable))

    return render(request, 'timetable_edit.html', {'form': timetable_form, 'timetable_detail_formset': timetable_detail_formset, 'timetable': timetable})


@restrict_access_to_local
def holidays(request):
    page = request.GET.get('page', 1)
    search_query = request.GET.get('search', '')
    if search_query:
        all_holidays = Holidays.objects.filter(year__icontains=search_query).order_by('-year')
    else:
        all_holidays = Holidays.objects.all().order_by('-year')

    holidays_with_count = []

    for holiday in all_holidays:
        count_of_details = HolidayDetails.objects.filter(holiday=holiday).count()
        holidays_with_count.append((holiday, count_of_details))

    settings = ConfigurationSettings.objects.latest('id')
    items_per_page = settings.rows_per_page
    paginator = Paginator(all_holidays, items_per_page)

    try:
        holidays = paginator.page(page)
    except PageNotAnInteger:
        holidays = paginator.page(1)
    except EmptyPage:
        holidays = paginator.page(paginator.num_pages)

    add_to_loop = ((holidays.number-1)*items_per_page)

    context = {
        'holidays': holidays,
        'holidays_with_count': holidays_with_count,
        'search_query': search_query,
        'add_to_loop': add_to_loop
    }

    return render(request, 'holidays.html', context)

@restrict_access_to_local
def holiday_edit(request, holiday_id):
    holiday = get_object_or_404(Holidays, pk=holiday_id) if holiday_id != 0 else Holidays()
    holiday_details = holiday.holidaydetails_set.all() if holiday_id != 0 else None
    # holiday_details = holiday.holiday_details.all()

    HolidayDetailFormSet = modelformset_factory(
        HolidayDetails, 
        form=HolidayDetailForm, 
        extra=1, 
        can_delete=True
    )

    if request.method == 'POST':
        if 'delete' in request.POST:
            # Handle delete action
            if holiday:
                holiday.delete()
                return redirect('holidays')  # Redirect after deletion
        else:
            holiday_form = HolidayForm(request.POST, instance=holiday)
            holiday_detail_formset = HolidayDetailFormSet(
                request.POST, 
                prefix='holiday_details', 
                queryset=HolidayDetails.objects.filter(holiday=holiday)
            )

            if holiday_form.is_valid() and holiday_detail_formset.is_valid():
                holiday = holiday_form.save()
                messages.success(request, 'Your changes saved successfully.')

                for form in holiday_detail_formset:
                    if form.cleaned_data.get('DELETE'):
                        form.instance.delete()
                    elif form.cleaned_data:
                        instance = form.save(commit=False)
                        instance.holiday = holiday
                        instance.save()


                return redirect('holiday_edit', holiday_id=holiday.id)
            
    else:
        holiday_form = HolidayForm(instance=holiday)
        holiday_detail_formset = HolidayDetailFormSet(prefix='holiday_details', queryset=HolidayDetails.objects.filter(holiday=holiday))

    return render(request, 'holiday_edit.html', {'form': holiday_form, 'holiday_detail_formset': holiday_detail_formset, 'holiday': holiday})