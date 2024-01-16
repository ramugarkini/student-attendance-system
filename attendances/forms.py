from django import forms
from .models import Attendances, AttendanceTimetableDetails, AttendanceTimetableDetailStudents

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendances
        fields = ['date', 'department', 'enrollment_year', 'section', 'weekday', 'timetable']

        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].widget.attrs['class'] = 'form-control'
        self.fields['enrollment_year'].widget.attrs['class'] = 'form-control'
        self.fields['section'].widget.attrs['class'] = 'form-control'
        self.fields['weekday'].widget.attrs['class'] = 'form-control'
        self.fields['timetable'].widget.attrs['class'] = 'form-control'


class AttendanceTimetableDetailForm(forms.ModelForm):
    class Meta:
        model = AttendanceTimetableDetails
        fields = '__all__'
        exclude = ['id', 'attendance']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['student'].widget.attrs['class'] = 'form-control'
        self.fields['timetable_detail'].widget.attrs['class'] = 'form-control'
        # self.fields['attendance_type'].widget.attrs['class'] = 'form-control'

class AttendanceTimetableDetailStudentForm(forms.ModelForm):
    class Meta:
        model = AttendanceTimetableDetailStudents
        fields = '__all__'
        exclude = ['id', 'attendance_timetable_detail']

        widgets = {
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].widget.attrs['class'] = 'form-control'
        # self.fields['timetable_detail'].widget.attrs['class'] = 'form-control'
        self.fields['attendance_type'].widget.attrs['class'] = 'form-control'