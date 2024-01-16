# students/models.py
from django.db import models
from masters.models import Departments, EnrollmentYears, Sections

class Students(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    roll_number = models.CharField(max_length=15)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    section = models.ForeignKey(Sections, on_delete=models.CASCADE)
    enrollment_year = models.ForeignKey(EnrollmentYears, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/students/', blank=True, null=True)
    face_encoding = models.BinaryField(blank=True, null=True)

    def __str__(self):
        # return f"Student {self.name} in Department {self.department} in EnrollmentYear {self.enrollment_year}"
        return f"{self.name} - {self.roll_number}"
