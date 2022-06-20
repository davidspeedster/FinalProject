from django.db import models
from authentication.models import User


# Create your models here.
MALE = "male"
FEMALE = "female"

SEX = (
    (MALE, "male"),
    (FEMALE, "female"),
)


class Hospital(models.Model):
    user = models.OneToOneField(
        User, related_name="hosptals", primary_key=True, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200, default=" ")
    email = models.EmailField(max_length=100, default=" ")
    city = models.CharField(max_length=100, default=" ")
    sub_city = models.CharField(max_length=100, default=" ")
    phone = models.CharField(max_length=20, default=" ")
    woreda = models.CharField(max_length=10, default=" ")
    isActive = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class RegisteredPersonnel(models.Model):
    user = models.OneToOneField(
        User, related_name="personnel", primary_key=True, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200, default=" ")
    email = models.EmailField(max_length=200, default=" ")
    phone = models.CharField(max_length=20, default=" ")
    city = models.CharField(max_length=100, default=" ")
    sub_city = models.CharField(max_length=100, default=" ")
    woreda = models.CharField(max_length=10, default=" ")
    profile_picture = models.ImageField(
        upload_to=upload_to, blank=True, null=True)
    description = models.TextField(max_length=500, default=" ")
    hospital = models.UUIDField(default=None, null=True)
    isActive = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)


class Patient(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    sex = models.CharField(max_length=20, choices=SEX)
    age = models.IntegerField(max_length=5)
    sub_city = models.CharField(max_length=100)
    woreda = models.CharField(max_length=10)
    bmi = models.FloatField(max_length=5)
    temperature = models.FloatField(max_length=5)
    blood_pressure = models.FloatField(max_length=5)
    rbc_count = models.FloatField(max_length=5)
    doctor = models.UUIDField(default=None, null=True)


class RequestDiagnostic(models.Model):

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    result = models.CharField(max_length=100, default="Pending")
    doctor = models.ForeignKey(
        RegisteredPersonnel, on_delete=models.CASCADE, related_name="Doctor")
    lab_technician = models.ForeignKey(
        RegisteredPersonnel, on_delete=models.CASCADE, related_name="Lab_Technician")


class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=200)
    doctor = models.ForeignKey(
        RegisteredPersonnel, on_delete=models.CASCADE)
    instruction = models.CharField(max_length=200)
