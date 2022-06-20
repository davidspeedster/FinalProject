from rest_framework import serializers
from malaria import models


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hospital
        fields = ['user_id', 'name', 'email', 'phone', 'city',
                  'sub_city', 'woreda', 'isActive', 'is_verified']


class RegisteredPersonnelSerializer(serializers.ModelSerializer):
    class Meta:

        model = models.RegisteredPersonnel
        fields = ['user_id', 'name', 'email', 'phone', 'city', 'sub_city', 'woreda',
                  'profile_picture', 'description', 'hospital', 'isActive', 'is_verified']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Patient
        fields = ['id', 'name', 'phone', 'city', 'sub_city', 'woreda',
                  'age', 'sex', 'rbc_count',
                  'bmi', 'blood_pressure', 'temperature']


class RequestDiagnosticSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RequestDiagnostic
        fields = ['id', 'patient', 'result', 'doctor',
                  'lab_technician']


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Prescription
        fields = ['id', 'patient_name', 'medicine_name', 'doctor_name',
                  'instruction', ]
