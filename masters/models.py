# masters/models.py
from django.db import models
from django.utils import timezone

class Departments(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"


class AcademicYears(models.Model):
    id = models.AutoField(primary_key=True)
    academic_year = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.academic_year}"

class EnrollmentYears(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=4)
    year = models.CharField(max_length=4)
    academic_year = models.ForeignKey(AcademicYears, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.year} - {self.academic_year}"

class Sections(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYears, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.department} - {self.academic_year}"

class SubjectDetails(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Timetables(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    section = models.ForeignKey(Sections, on_delete=models.CASCADE)
    # academic_year = models.ForeignKey(AcademicYears, on_delete=models.CASCADE)
    enrollment_year = models.ForeignKey(EnrollmentYears, on_delete=models.CASCADE)
    
    WEEKDAY_CHOICES = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    ]

    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, default=1)

    def __str__(self):
        # return f"Timetable for Department {self.department} in EnrollmentYear {self.enrollment_year}"
        return f"{self.enrollment_year.academic_year.academic_year} - {self.department.name}-{self.section.name}"

class TimetableDetails(models.Model):
    id = models.AutoField(primary_key=True)
    timetable = models.ForeignKey(Timetables, on_delete=models.CASCADE)
    # timetable = models.ForeignKey(Timetables, on_delete=models.CASCADE, related_name='timetable_details')
    period_no = models.IntegerField()
    subject_detail = models.ForeignKey(SubjectDetails, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        # return f"TimetableDetails for {self.timetable} - Period {self.period_no} - {self.subject_detail.name if self.subject_detail else 'None'}"
        return f"{self.period_no}. {self.subject_detail.code} ({self.start_time} - {self.end_time})"

class Holidays(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.year}"

class HolidayDetails(models.Model):
    id = models.AutoField(primary_key=True)
    holiday = models.ForeignKey(Holidays, on_delete=models.CASCADE)
    date = models.DateField()
    holiday_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.date} - {self.holiday_name}"