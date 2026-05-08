from django.db import models

from django.contrib.auth.models import User


class Department(models.Model):
    dep_name = models.CharField(max_length=100)
    dep_description = models.TextField()

    def __str__(self):
        return self.dep_name


class Doctors(models.Model):
    doc_name = models.CharField(max_length=100)
    doc_spec = models.CharField(max_length=100)
    dep_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    dep_image = models.ImageField(upload_to='doctors/')

    def __str__(self):
        return self.doc_name
     
class Booking(models.Model):
    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    patient_phone = models.CharField(max_length=20)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time =  models.TimeField()

    def __str__(self):
        return f"{self.patient_name} - {self.doctor.doc_name} "
    

class Profile(models.Model):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username




class Report(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.FileField(upload_to='reports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)