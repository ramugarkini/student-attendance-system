# students/forms.py
from django import forms
from .models import Students

class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['name', 'roll_number', 'department', 'section', 'enrollment_year', 'mobile_no', 'email', 'remarks', 'image']

    # remove_image = forms.BooleanField(required=False, widget=forms.HiddenInput())

