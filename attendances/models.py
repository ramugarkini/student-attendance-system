from django.db import models
from masters.models import Departments, EnrollmentYears, Sections, Timetables, TimetableDetails
from students.models import Students
# from django.db.models.functions import Now

class Attendances(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(null=True)
    # time = models.TimeField(null=True)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    enrollment_year = models.ForeignKey(EnrollmentYears, on_delete=models.CASCADE)
    # academic_year = models.ForeignKey(AcademicYears, on_delete=models.CASCADE)
    section = models.ForeignKey(Sections, on_delete=models.CASCADE)

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

    # timetable_detail = models.ForeignKey(TimetableDetails, on_delete=models.CASCADE)
    timetable = models.ForeignKey(Timetables, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.date} - {self.time}"

class AttendanceTimetableDetails(models.Model):
    id = models.AutoField(primary_key=True)
    attendance = models.ForeignKey(Attendances, on_delete=models.CASCADE)
    # date = models.DateField(null=True)
    # time = models.TimeField(null=True)
    timetable_detail = models.ForeignKey(TimetableDetails, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.student} - {self.date} {self.time}"

class AttendanceTimetableDetailStudents(models.Model):
    id = models.AutoField(primary_key=True)
    attendance_timetable_detail = models.ForeignKey(AttendanceTimetableDetails, on_delete=models.CASCADE)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)

    ATTENDANCE_TYPE_CHOICES = [
        (1, 'Manual'),
        (2, 'Face Scan'),
    ]
    attendance_type = models.IntegerField(choices=ATTENDANCE_TYPE_CHOICES, default=1)

    def __str__(self):
        return f"{self.student} - {self.date} {self.time}"