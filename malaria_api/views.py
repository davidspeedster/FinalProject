from malaria import models
from malaria_api import serializers
from rest_framework import generics, permissions
import coreapi
from rest_framework.schemas import AutoSchema
from authentication import custom_permissions
from authentication.models import User
from authentication.serializers import UserSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class MalariaViewSchema(AutoSchema):

    def get_manual_fields(self, path, method):
        extra_fields = []
        if method.lower() in ['post', 'put']:
            extra_fields = [
                coreapi.Field('desc')
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields


class HospitalList(generics.ListAPIView):
    schema = MalariaViewSchema()
    permission_classes = [
        permissions.IsAuthenticated]
    queryset = models.Hospital.objects.all()
    serializer_class = serializers.HospitalSerializer


class HospitalDetail(generics.RetrieveUpdateDestroyAPIView):
    schema = MalariaViewSchema()
    permission_classes = [
        permissions.IsAuthenticated & (custom_permissions.isAdmin | custom_permissions.hasWritePermission)]
    queryset = models.Hospital.objects.all()
    serializer_class = serializers.HospitalSerializer


class RegisteredPersonnelList(generics.ListAPIView):
    schema = MalariaViewSchema()
    serializer_class = serializers.RegisteredPersonnelSerializer

    def get_queryset(self):
        queryset = models.RegisteredPersonnel.objects.all()
        user_id = self.request.query_params.get('id')
        queryset = queryset.filter(hospital__user_id=user_id)
        return queryset
    permission_classes = [permissions.IsAuthenticated &
                          custom_permissions.isEmployee & custom_permissions.isVerifiedHospital]


class DoctorList(generics.ListAPIView):
    schema = MalariaViewSchema()
    serializer_class = serializers.RegisteredPersonnelSerializer

    def get_queryset(self):
        hospital_id = self.request.query_params.get('hospital_id')
        queryset = models.RegisteredPersonnel.objects.all()
        queryset = queryset.filter(
            user__role="doctor", hospital=hospital_id)
        return queryset
    permission_classes = [permissions.IsAuthenticated &
                          custom_permissions.isVerifiedPersonnel]


class RegisteredPersonnelDetail(generics.RetrieveUpdateAPIView):
    schema = MalariaViewSchema()
    queryset = models.RegisteredPersonnel.objects.all()
    serializer_class = serializers.RegisteredPersonnelSerializer
    permission_classes = []
    parser_classes = (JSONParser, FormParser, MultiPartParser)


class ReceptionistPatientList(generics.ListCreateAPIView):
    schema = MalariaViewSchema()
    permission_classes = [permissions.IsAuthenticated &
                          custom_permissions.isReceptionist & custom_permissions.isOwnerPersonnel & custom_permissions.isVerifiedPersonnel]

    def get_queryset(self):
        queryset = models.Patient.objects.all()
        hospital = self.request.query_params.get('hospital')
        queryset = queryset.filter(hospital=hospital)
        return queryset

    serializer_class = serializers.PatientSerializer


class ReceptionistPatientDetail(generics.RetrieveUpdateDestroyAPIView):
    schema = MalariaViewSchema()

    permission_classes = [permissions.IsAuthenticated &
                          custom_permissions.isReceptionist & custom_permissions.isOwnerPersonnel & custom_permissions.isVerifiedPersonnel]

    def get_queryset(self):
        queryset = models.Patient.objects.all()
        hospital = self.request.query_params.get('hospital')
        queryset = queryset.filter(hospital=hospital)
        return queryset

    serializer_class = serializers.PatientSerializer


class DoctorPatientList(generics.ListAPIView):
    schema = MalariaViewSchema()

    permission_classes = [permissions.IsAuthenticated &
                          custom_permissions.isDoctor & custom_permissions.isDoctorOfPatient & custom_permissions.isOwnerPersonnel & custom_permissions.isVerifiedPersonnel]

    def get_queryset(self):
        queryset = models.Patient.objects.all()
        user_id = self.request.query_params.get('id')
        queryset = queryset.filter(doctor__user_id=user_id)
        return queryset
    serializer_class = serializers.PatientSerializer


class DoctorPatientDetail(generics.RetrieveUpdateAPIView):
    schema = MalariaViewSchema()

    permission_classes = [permissions.IsAuthenticated &
                          custom_permissions.isDoctor & custom_permissions.isDoctorOfPatient & custom_permissions.isOwnerPersonnel & custom_permissions.isVerifiedPersonnel]

    def get_queryset(self):
        queryset = models.Patient.objects.all()
        user_id = self.request.query_params.get('id')
        queryset = queryset.filter(doctor__user_id=user_id)
        return queryset
    serializer_class = serializers.PatientSerializer


class RequestDiagnosticList(generics.ListCreateAPIView):
    schema = MalariaViewSchema()
    permission_classes = [permissions.IsAuthenticated &
                          custom_permissions.isDoctor & custom_permissions.isVerifiedPersonnel]

    def get_queryset(self):
        queryset = models.RequestDiagnostic.objects.all()
        user_id = self.request.query_params.get('id')
        queryset = queryset.filter(doctor__user_id=user_id)
        return queryset
    serializer_class = serializers.RequestDiagnosticSerializer


class RequestDiagnosticDetail(generics.RetrieveUpdateDestroyAPIView):
    schema = MalariaViewSchema()
    permission_classes = [permissions.IsAuthenticated &
                          custom_permissions.isDoctor & custom_permissions.isVerifiedPersonnel]

    def get_queryset(self):
        queryset = models.RequestDiagnostic.objects.all()
        user_id = self.request.query_params.get('id')
        queryset = queryset.filter(doctor__user_id=user_id)
        return queryset
    serializer_class = serializers.RequestDiagnosticSerializer


class SetDiagnosticResult(generics.RetrieveUpdateAPIView):
    schema = MalariaViewSchema()
    permission_classes = [permissions.IsAuthenticated &
                          custom_permissions.isLabTech & custom_permissions.isVerifiedPersonnel]

    def get_queryset(self):
        queryset = models.RequestDiagnostic.objects.all()
        user_id = self.request.query_params.get('id')
        queryset = queryset.filter(lab_technician__user_id=user_id)
        return queryset
    serializer_class = serializers.RequestDiagnosticSerializer


class PrescriptionList(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated &
                          custom_permissions.isDoctor & custom_permissions.isVerifiedPersonnel]
    schema = MalariaViewSchema()

    def get_queryset(self):
        queryset = models.RequestDiagnostic.objects.all()
        user_id = self.request.query_params.get('id')
        queryset = queryset.filter(doctor__user_id=user_id)
        return queryset
    serializer_class = serializers.PrescriptionSerializer


class PrescriptionDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated &
                          custom_permissions.isDoctor & custom_permissions.isPrescriptionOfDoctor & custom_permissions.isVerifiedPersonnel]
    schema = MalariaViewSchema()

    def get_queryset(self):
        queryset = models.RequestDiagnostic.objects.all()
        user_id = self.request.query_params.get('id')
        queryset = queryset.filter(doctor__user_id=user_id)
        return queryset
    serializer_class = serializers.PrescriptionSerializer
