# masters/forms.py
from django import forms
from .models import Departments, EnrollmentYears, AcademicYears, Sections, Subjects, SubjectDetails, Timetables, TimetableDetails, Holidays, HolidayDetails

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Departments
        fields = ['code', 'name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['class'] = 'form-control'

class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYears
        fields = ['academic_year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['academic_year'].widget.attrs['class'] = 'form-control'

class EnrollmentYearForm(forms.ModelForm):
    class Meta:
        model = EnrollmentYears
        fields = ['code', 'year', 'academic_year']

    year = forms.IntegerField(
        widget=forms.Select(choices=[], attrs={'class': 'form-control'}),
        label='Year'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['year'].widget.choices = self.get_year_choices()
        self.fields['code'].widget.attrs['class'] = 'form-control'
        self.fields['academic_year'].widget.attrs['class'] = 'form-control'


    def get_year_choices(self):
        return [(year, str(year)) for year in range(2019, 2031)]


class SectionForm(forms.ModelForm):
    class Meta:
        model = Sections
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subjects
        fields = ['department', 'academic_year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].widget.attrs['class'] = 'form-control'
        self.fields['academic_year'].widget.attrs['class'] = 'form-control'

class SubjectDetailForm(forms.ModelForm):
    class Meta:
        model = SubjectDetails
        fields = '__all__'
        exclude = ['id', 'subject']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['class'] = 'form-control'

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetables
        fields = ['department', 'section', 'enrollment_year', 'weekday']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].widget.attrs['class'] = 'form-control'
        self.fields['section'].widget.attrs['class'] = 'form-control'
        self.fields['enrollment_year'].widget.attrs['class'] = 'form-control'
        self.fields['weekday'].widget.attrs['class'] = 'form-control'
        # self.fields[''].widget = forms.HiddenInput()

class TimetableDetailForm(forms.ModelForm):
    class Meta:
        model = TimetableDetails
        # fields = ['timetable', 'subject_detail', 'period_no', 'start_time', 'end_time']
        fields = '__all__'
        exclude = ['id', 'timetable']

        widgets = {
            # 'timetable': forms.HiddenInput(),
            # 'DELETE': forms.HiddenInput(),
            'start_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['period_no'].widget.attrs['class'] = 'form-control'
        self.fields['subject_detail'].widget.attrs['class'] = 'form-control subject_detail'

        # # Filter SubjectDetails based on the department of the associated Timetable
        # timetable = self.instance.timetable if self.instance and hasattr(self.instance, 'timetable') else None

        # if timetable and timetable.department:
        #     academic_year = timetable.enrollment_year.current_academic_year if timetable.enrollment_year else None

        #     if academic_year:
        #         self.fields['subject_detail'].queryset = (
        #             SubjectDetails.objects.filter(
        #                 subject__department=timetable.department,
        #                 subject__academic_year=academic_year
        #             )
        #         )
        #     else:
        #         # Handle the case when academic_year is not available
        #         # Set the queryset to an empty list or the desired default behavior
        #         self.fields['subject_detail'].queryset = SubjectDetails.objects.none()
        # else:
        #     # Handle the case when timetable or department is not available
        #     # Set the queryset to an empty list or the desired default behavior
        #     self.fields['subject_detail'].queryset = SubjectDetails.objects.none()

class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holidays
        fields = ['year']

    year = forms.IntegerField(
        widget=forms.Select(choices=[], attrs={'class': 'form-control'}),
        label='Year'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate the year choices dynamically based on your requirements
        self.fields['year'].widget.choices = self.get_year_choices()

    def get_year_choices(self):
        # Customize this method to provide the list of year choices you want
        # For example, if you want to provide the range of years from 2020 to 2030
        return [(year, str(year)) for year in range(2019, 2031)]

class HolidayDetailForm(forms.ModelForm):
    class Meta:
        model = HolidayDetails
        fields = '__all__'
        exclude = ['id', 'holiday']

        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'holiday_name': forms.TextInput(attrs={'class': 'form-control'}),
        }